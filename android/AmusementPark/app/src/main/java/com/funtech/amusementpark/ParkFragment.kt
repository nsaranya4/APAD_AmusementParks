package com.funtech.amusementpark

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.funtech.amusementpark.models.Park
import java.util.*
import kotlin.collections.ArrayList

class ParkFragment : Fragment() {

    private val image1 = "https://firebasestorage.googleapis.com/v0/b/funtech-frontend.appspot.com/o/images%2Fcedar_point.jpg?alt=medias"
    private val image2 = "https://firebasestorage.googleapis.com/v0/b/funtech-frontend.appspot.com/o/images%2F7LK169PFGWMPL3H6CWMK02VNNTJSEW4W?alt=media"
    private val image3 = "https://images.pexels.com/photos/1067333/pexels-photo-1067333.jpeg"
    private val image4 = "https://firebasestorage.googleapis.com/v0/b/funtech-frontend.appspot.com/o/images%2Funiversal_s.jpg?alt=media"
    private val image5 = "https://firebasestorage.googleapis.com/v0/b/funtech-frontend.appspot.com/o/images%2Fwonderla_hyd.jpg?alt=media"

    private var parks = ArrayList<Park>(
        Arrays.asList(
            Park(image1, "EsselWorld1", "EsselWorld desc"),
            Park(image2, "EsselWorld2", "EsselWorld desc"),
            Park(image3, "EsselWorld3", "EsselWorld desc"),
            Park(image4, "EsselWorld4", "EsselWorld desc"),
            Park(image5, "EsselWorld5", "EsselWorld desc")
        )
    )
    private lateinit var linearLayoutManager: LinearLayoutManager
    private lateinit var adapter: ParkRecyclerAdapter

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_park, container, false)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        adapter = ParkRecyclerAdapter(parks)
        linearLayoutManager = LinearLayoutManager(activity, LinearLayoutManager.VERTICAL, false)
        var recyclerView = view.findViewById(R.id.park_recycler_view) as RecyclerView
        recyclerView.adapter = adapter
        recyclerView.layoutManager = linearLayoutManager
    }

    companion object {
        fun newInstance(): ParkFragment = ParkFragment()
    }
}