package com.funtech.amusementpark

import android.util.Log
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.RecyclerView
import com.funtech.amusementpark.models.Park
import com.squareup.picasso.Picasso
import kotlinx.android.synthetic.main.park_item.view.*

class ParkRecyclerAdapter(private val parks: ArrayList<Park>):
    RecyclerView.Adapter<ParkRecyclerAdapter.ParkHolder>() {

    override fun onCreateViewHolder(parent: ViewGroup, viewType: Int): ParkHolder {
        val inflatedView = parent.inflate(R.layout.park_item, false)
        return ParkHolder(inflatedView)
    }

    override fun getItemCount(): Int = parks.size

    override fun onBindViewHolder(holder: ParkRecyclerAdapter.ParkHolder, position: Int) {
        val park = parks[position]
        holder.bindPark(park)
    }

    class ParkHolder(private val view: View) : RecyclerView.ViewHolder(view), View.OnClickListener {
        private var park: Park? = null

        init {
            view.setOnClickListener(this)
        }

        fun bindPark(park: Park) {
            this.park = park
            Picasso.with(view.context).load(park.image_id).into(view.park_image)
            view.park_name.text = park.name
            view.park_description.text = park.description
        }

        override fun onClick(v: View) {
            Log.d("RecyclerView", "CLICK!")
        }

        companion object {
            private val PARK_KEY = "PARK"
        }
    }

}