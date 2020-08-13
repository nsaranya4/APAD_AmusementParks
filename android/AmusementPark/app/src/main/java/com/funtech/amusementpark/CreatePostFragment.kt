package com.funtech.amusementpark

import android.content.Context
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.location.Location
import android.location.LocationManager
import android.os.Bundle
import android.os.Looper
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Toast
import androidx.core.app.ActivityCompat
import androidx.navigation.fragment.navArgs
import com.funtech.amusementpark.models.CreatePostRequest
import com.funtech.amusementpark.models.Post
import com.funtech.amusementpark.services.Network
import com.google.android.gms.location.*
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class CreatePostFragment : Fragment() {
    private lateinit var parkId: String
    private lateinit var userId: String
    val args: PostFragmentArgs by navArgs()
    lateinit var fusedLocationProviderClient: FusedLocationProviderClient
    lateinit var locationRequest: LocationRequest


    private fun getUserIdFromSharedPreferences(context: Context) : String {
        var sharedPreferences = context.getSharedPreferences("funtech", Context.MODE_PRIVATE);
        val userId = sharedPreferences.getString("user_id", null)
        return userId!!
    }

    private fun createPost(context: Context, createPostRequest: CreatePostRequest) {
        var postCall : Call<Post> = Network.postService.createPost(createPostRequest)
        postCall.enqueue(object : Callback<Post> {
            override fun onResponse(call : Call<Post>, response: Response<Post>)
            {
                if (response.isSuccessful) {
                    val user = response.body()!!
                }
                else {
                    Log.e(TAG, "Failed to get user by email from backend")
                }
            }

            override fun onFailure(call: Call<Post>, t: Throwable) {
                Log.e(TAG, "Failed to get user by email from backend")
            }
        })
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        parkId = args.parkId
        userId = getUserIdFromSharedPreferences(view.context)
        Log.d(TAG, userId)
        Log.d(TAG, parkId)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        return inflater.inflate(R.layout.fragment_create_post, container, false)
    }


    fun getLastLocation(){
        //first we check permission
        if(CheckPermission()){
            //check if location servise enabled
            if(isLocationEnabled()){
                //Get location
                fusedLocationProviderClient.lastLocation.addOnCompleteListener {task->
                    var location: Location? = task.result
                    if(location == null){
                        //if location is null get new user location
                        getNewLocation()
                    }else{
                        textView_location.text = "You Current Location is : \nLat:" + location.latitude + " ; Long:" + location.longitude
                    }
                }
            }else{
                Toast.makeText(this,"Please Turn on Location Services", Toast.LENGTH_SHORT).show()
            }
        }else{
            RequestPermission()
        }
    }


    fun getNewLocation(){
        var locationRequest =  LocationRequest()
        locationRequest.priority = LocationRequest.PRIORITY_HIGH_ACCURACY
        locationRequest.interval = 0
        locationRequest.fastestInterval = 0
        locationRequest.numUpdates = 1
        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(this)
        fusedLocationProviderClient!!.requestLocationUpdates(locationRequest,locationCallback, Looper.myLooper())
    }

    //create location callback variable
    private val locationCallback = object : LocationCallback(){
        override fun onLocationResult(locationResult: LocationResult) {
            var lastLocation: Location = locationResult.lastLocation
            //set new location
           // textView_location.text = "Your Current Location is : \nLat:" + lastLocation.latitude + " ; Long:" + lastLocation.longitude
        }
    }



    //first we need to create a function that will check the user permission
    fun CheckPermission():Boolean{
        //this function will return a boolean
        //true: if we have permission
        //false if not
        if(
            ActivityCompat.checkSelfPermission(this,android.Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED ||
            ActivityCompat.checkSelfPermission(this,android.Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
        ){
            return true
        }

        return false

    }

    //Now we need to create a function that will allow us to get user permission
    fun RequestPermission(){
        //this function will allows us to tell the user to requesut the necessary permsiion if they are not garented
        ActivityCompat.requestPermissions(
            this,
            arrayOf(android.Manifest.permission.ACCESS_COARSE_LOCATION,android.Manifest.permission.ACCESS_FINE_LOCATION),
            PERMISSION_ID
        )
    }

    //Now we need a function that checks if the location service of the device is enabled
    fun isLocationEnabled():Boolean{
        //this function will return to us the state of the location service
        //if the gps or the network provider is enabled then it will return true otherwise it will return false
        var locationManager = getSystemService(Context.LOCATION_SERVICE) as LocationManager
        return locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER) || locationManager.isProviderEnabled(
            LocationManager.NETWORK_PROVIDER)
    }

    override fun onRequestPermissionsResult(
        requestCode: Int,
        permissions: Array<out String>,
        grantResults: IntArray
    ) {
        //this is a built-in function that check the permission result
        if(requestCode == PERMISSION_ID){
            if(grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED){
                Log.d("Debug:", "You have the permission")
            }
        }

    }






    companion object {
        private val TAG = "CREATE_POST_FRAGMENT"
        fun newInstance(): CreatePostFragment = CreatePostFragment()
        private val PERMISSION_ID = 10
    }
}