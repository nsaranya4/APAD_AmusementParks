package com.funtech.amusementpark

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Color
import android.location.Location
import android.location.LocationManager
import android.net.Uri
import android.os.Bundle
import android.os.Looper
import android.text.Editable
import android.text.TextWatcher
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.*
import androidx.core.app.ActivityCompat
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import com.esafirm.imagepicker.features.ImagePicker
import com.esafirm.imagepicker.features.ReturnMode
import com.esafirm.imagepicker.model.Image
import com.funtech.amusementpark.models.CreatePostRequest
import com.funtech.amusementpark.models.Post
import com.funtech.amusementpark.services.Network
import com.google.android.gms.location.*
import com.google.firebase.storage.FirebaseStorage
import com.google.firebase.storage.StorageReference
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.fragment_create_post.view.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import java.io.File
import com.funtech.amusementpark.models.Location as MyLocation

class CreatePostFragment : Fragment() {
    private val alphabet: List<Char> = ('A'..'Z') + ('0'..'9')
    private lateinit var parkId: String
    private lateinit var userId: String
    private lateinit var createPostButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var fusedLocationProviderClient: FusedLocationProviderClient
    val args: PostFragmentArgs by navArgs()

    // Input fields to be populated
    private lateinit var title: EditText
    private lateinit var description: EditText
    private lateinit var tags: EditText
    private var lat: Double? = null
    private var lng: Double? = null
    private lateinit var image: Image
    private lateinit var imageView: ImageView


    private fun getTextWatcher(editText: EditText) : TextWatcher {
        return object : TextWatcher {
            override fun beforeTextChanged(charSequence: CharSequence, i: Int, i1: Int, i2: Int) {}
            override fun onTextChanged(charSequence: CharSequence, i: Int, i1: Int, i2: Int) {}
            override fun afterTextChanged(editable: Editable) {
                checkIfDataIsPopulated()
            }
        }
    }




    private fun checkIfDataIsPopulated() {
        Log.d(TAG, "checkIfDataIsPopulated")
        if (title.text.toString() != null
            && description.text.toString() != null
            && tags.text.toString() != null
            && image != null && image.path != null) {
            createPostButton.isEnabled = true
        }
    }



    private fun getUserIdFromSharedPreferences(context: Context) : String {
        var sharedPreferences = context.getSharedPreferences("funtech", Context.MODE_PRIVATE);
        val userId = sharedPreferences.getString("user_id", null)
        return userId!!
    }

    private fun createPost(createPostRequest: CreatePostRequest) {
        var postCall : Call<Post> = Network.postService.createPost(createPostRequest)
        postCall.enqueue(object : Callback<Post> {

            override fun onResponse(call : Call<Post>, response: Response<Post>)
            {
                if (response.isSuccessful) {
                    progressBar.visibility = View.GONE
                    val action = CreatePostFragmentDirections.actionCreatePostFragmentToPostFragment(parkId)
                    findNavController().navigate(action)
                }
                else {
                    Log.e(TAG, "Failed to create post")
                }
            }

            override fun onFailure(call: Call<Post>, t: Throwable) {
                Log.e(TAG, "Failed to create post")
            }
        })
    }

    private fun takeImage() {
        ImagePicker.create(this)
            .returnMode(ReturnMode.ALL)
            .folderMode(true)
            .toolbarFolderTitle("Folder")
            .toolbarImageTitle("Tap to select")
            .toolbarArrowColor(Color.BLACK)
            .single()
            .showCamera(true)
            .imageDirectory("Camera")
            .start();
    }

    private fun generateImageId(): String {
        val imageId = List(32) { alphabet.random() }.joinToString("")
        Log.d(TAG, "imageid= " + imageId)
        return imageId
    }

    private fun uploadImageAndCreatePost(createPostRequest: CreatePostRequest)  {
        val storageRef = FirebaseStorage.getInstance().reference
        var imagesRef: StorageReference = storageRef.child(createPostRequest.image_id)
        val filePath: Uri = Uri.fromFile(File(image.path))
        imagesRef.putFile(filePath)
            .addOnSuccessListener {
                createPost(createPostRequest)
            }.addOnFailureListener {
                Log.e(TAG, "Failed to upload image")
            }
    }


    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        if (ImagePicker.shouldHandle(requestCode, resultCode, data)) {
            val pickedImage: Image = ImagePicker.getFirstImageOrNull(data)
            Log.d(TAG, pickedImage.name)
            image = pickedImage
            imageView.visibility = View.VISIBLE
            val filePath: Uri = Uri.fromFile(File(image.path))
            Picasso.with(context).load(filePath).into(imageView)
        }
        super.onActivityResult(requestCode, resultCode, data)
    }


    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        parkId = args.parkId
        userId = getUserIdFromSharedPreferences(view.context)
        Log.d(TAG, userId)
        Log.d(TAG, parkId)

        val gpsButton = view.findViewById(R.id.gps_button) as ImageButton
        gpsButton.setOnClickListener {
            Log.d(TAG, "GPS Button clicked")
            getLastLocation(view.context)
        }

        val cameraButton = view.findViewById(R.id.camera_button) as ImageButton
        cameraButton.setOnClickListener {
            Log.d(TAG, "camera Button clicked")
            takeImage()
        }

        title = view.findViewById(R.id.title_input) as EditText
        description = view.findViewById(R.id.description_input) as EditText
        tags = view.findViewById(R.id.tags_input) as EditText

//        Register edit text to see if we want to enable the create button
//        title.addTextChangedListener(getTextWatcher(title));
//        description.addTextChangedListener(getTextWatcher(description));
//        tags.addTextChangedListener(getTextWatcher(tags));
//        Log.d(TAG, "added text edit listener")

        imageView = view.findViewById(R.id.create_post_image) as ImageView
        progressBar = view.findViewById(R.id.create_post_loading) as ProgressBar
        createPostButton = view.findViewById(R.id.create_post_button) as Button
//        createPostButton.isEnabled = false
        createPostButton.setOnClickListener {
            Log.d(TAG, "create Post Button clicked")
            createPostButton.visibility = View.GONE
            progressBar.visibility = View.VISIBLE
            val title = view.title_input.text.toString()
            val imageId = "images/" + generateImageId()
            val description = view.description_input.text.toString()
            val location = MyLocation(lat!!, lng!!)
            val tags = view.tags_input.text.toString().split(",").map { it.trim() }
            val createPostRequest =  CreatePostRequest(title = title, tags = tags,
                image_id = imageId, description = description,
                location = location, user_id = userId, park_id = parkId)
            uploadImageAndCreatePost(createPostRequest)
        }

    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val myActivity = activity as Activity
        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(myActivity)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_create_post, container, false)
    }

    private fun getLastLocation(context: Context) {
        if(checkPermission(context)) {
            if(isLocationEnabled(context)) {
                fusedLocationProviderClient.lastLocation.addOnCompleteListener { task ->
                        var location: Location? = task.result
                        if (location == null) {
                            getNewLocation()
                        } else {
                            val locationMsg = "Latitude: " + location.latitude + " ,Longitude: " + location.longitude
                            Toast.makeText(context, locationMsg, Toast.LENGTH_LONG).show()
                            lat = location.latitude
                            lng = location.longitude
                    }
                }
            } else {

            }
        } else {
            requestPermission()
        }
    }

    @SuppressLint("MissingPermission")
    private fun getNewLocation() {
        var locationRequest =  LocationRequest()
        locationRequest.priority = LocationRequest.PRIORITY_HIGH_ACCURACY
        locationRequest.interval = 0
        locationRequest.fastestInterval = 0
        locationRequest.numUpdates = 1
        fusedLocationProviderClient!!.requestLocationUpdates(locationRequest,locationCallback, Looper.myLooper())
    }

    private val locationCallback = object : LocationCallback() {
        override fun onLocationResult(locationResult: LocationResult) {
            val locationMsg = "Latitude: " + locationResult.lastLocation.latitude + " ,Longitude: " + locationResult.lastLocation.longitude
            Toast.makeText(context, locationMsg, Toast.LENGTH_LONG).show()
            var lastLocation: Location = locationResult.lastLocation
            lat = lastLocation.latitude
            lng = lastLocation.longitude
            val msg = "You Current Location is : \nLat:" + lastLocation.latitude + " ; Long:" + lastLocation.longitude
            Log.d(TAG,msg)
        }
    }


    private fun checkPermission(context: Context): Boolean {
        if( ActivityCompat.checkSelfPermission(context, android.Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED ||
            ActivityCompat.checkSelfPermission(context, android.Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED){
            return true
        }
        return false
    }

    private fun requestPermission() {
        requestPermissions(arrayOf(android.Manifest.permission.ACCESS_COARSE_LOCATION,
            android.Manifest.permission.ACCESS_FINE_LOCATION), PERMISSION_ID);
    }

    private fun isLocationEnabled(context: Context): Boolean {
        var locationManager = context.getSystemService(Context.LOCATION_SERVICE) as LocationManager
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(
            LocationManager.NETWORK_PROVIDER)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        if(requestCode == PERMISSION_ID){
            if(grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                Log.d(TAG, "You have the GPS permission")
            }
        }

    }
    companion object {
        private val TAG = "CREATE_POST_FRAGMENT"
        fun newInstance(): CreatePostFragment = CreatePostFragment()
        private val PERMISSION_ID = 10
    }
}