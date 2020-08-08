package com.funtech.amusementpark

import android.os.Bundle
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.fragment.app.Fragment
import androidx.recyclerview.widget.GridLayoutManager
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.ListAdapter
import androidx.recyclerview.widget.RecyclerView
import com.funtech.amusementpark.models.Park
import java.util.*
import kotlin.collections.ArrayList

class ParkFragment : Fragment() {

    private val image = "https://firebasestorage.googleapis.com/v0/b/funtech-frontend.appspot.com/o/images%2Fessel.png?alt=media"
    private var parks = ArrayList<Park>(
        Arrays.asList(
            Park(image, "EsselWorld1", "EsselWorld desc"),
            Park(image, "EsselWorld2", "EsselWorld desc"),
            Park(image, "EsselWorld3", "EsselWorld desc"),
            Park(image, "EsselWorld4", "EsselWorld desc"),
            Park(image, "EsselWorld5", "EsselWorld desc")
        )
    )
    private lateinit var linearLayoutManager: LinearLayoutManager
    private lateinit var adapter: ParkRecyclerAdapter


    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        var inflatedView = inflater.inflate(R.layout.fragment_park, container, false)
        var recyclerView = inflatedView.findViewById(R.id.park_recycler_view) as RecyclerView
        adapter = ParkRecyclerAdapter(parks)
        linearLayoutManager = LinearLayoutManager(activity, LinearLayoutManager.VERTICAL, false)
        recyclerView.adapter = adapter
        recyclerView.layoutManager = linearLayoutManager
        return inflatedView
    }



    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)

    }

    companion object {
        fun newInstance(): ParkFragment = ParkFragment()
    }
}