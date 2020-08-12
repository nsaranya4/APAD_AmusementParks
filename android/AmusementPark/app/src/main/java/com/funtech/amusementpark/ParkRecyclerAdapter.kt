package com.funtech.amusementpark

import android.content.Context
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.NavController
import androidx.recyclerview.widget.RecyclerView
import com.funtech.amusementpark.models.Park
import com.funtech.amusementpark.models.User
import com.google.firebase.storage.FirebaseStorage
import com.google.firebase.storage.StorageReference
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.park_item.view.*

class ParkRecyclerAdapter(private val parks: ArrayList<Park>,
                          private val context: Context,
                          private val navController: NavController): RecyclerView.Adapter<ParkRecyclerAdapter.ParkHolder>() {


    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ParkHolder {
        val inflatedView = LayoutInflater.from(context).inflate(R.layout.park_item, parent, false)
        return ParkHolder(inflatedView, navController)
    }

    override fun getItemCount(): Int = parks.size

    override fun onBindViewHolder(holder: ParkRecyclerAdapter.ParkHolder, position: Int) {
        val park = parks[position]
        holder.bindPark(park)
    }

    class ParkHolder(private val view: View, private val navController: NavController) : RecyclerView.ViewHolder(view), View.OnClickListener {
        private var park: Park? = null

        init {
            view.setOnClickListener(this)
        }

        fun bindPark(park: Park) {
            this.park = park
            val storageRef = FirebaseStorage.getInstance().getReference()
            var imagesRef: StorageReference = storageRef.child(park.image_id)
            imagesRef.downloadUrl.addOnSuccessListener { uri ->
                Log.d(TAG, uri.toString())
                Picasso.with(view.context).load(uri).into(view.park_image)
            }.addOnFailureListener {
                Log.e(TAG, "Failed to get download url")
            }
            view.park_name.text = park.name
            view.park_description.text = park.description
            view.park_user.text = park.user.name
        }

        override fun onClick(v: View) {
            Log.d(TAG, "Onclick")
            val action = ParkFragmentDirections.actionParkFragmentToPostFragment(this.park!!.id)
            navController.navigate(action)
        }

        companion object {
            private val PARK_KEY = "PARK"
            private val TAG = "PARK_RECYLER_ADAPTER"
        }
    }

}