package com.funtech.amusementpark

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
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
import android.widget.Button
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

        val gpsButton = view.findViewById(R.id.gps_button) as Button
        gpsButton.setOnClickListener {
            Log.d(TAG, "GPS Button clicked")
            getLastLocation(view.context)
        }
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

    private fun getLastLocation(context: Context) {
        if(checkPermission(context)) {
            if(isLocationEnabled(context)) {
                fusedLocationProviderClient.lastLocation.addOnCompleteListener { task ->
                    var location: Location? = task.result
                    if(location == null){
                        getNewLocation()
                    } else {
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
        val activity = getActivity() as Activity
        fusedLocationProviderClient = LocationServices.getFusedLocationProviderClient(activity)
        fusedLocationProviderClient!!.requestLocationUpdates(locationRequest,locationCallback, Looper.myLooper())
    }

    private val locationCallback = object : LocationCallback() {
        override fun onLocationResult(locationResult: LocationResult) {
            var lastLocation: Location = locationResult.lastLocation
            val msg = "You Current Location is : \nLat:" + lastLocation.latitude + " ; Long:" + lastLocation.longitude
            Log.d(TAG,msg)
        }
    }


    private fun checkPermission(context: Context): Boolean{
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