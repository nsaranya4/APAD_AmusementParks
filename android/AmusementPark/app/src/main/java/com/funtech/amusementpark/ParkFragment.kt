package com.funtech.amusementpark

import android.app.Activity
import android.os.Bundle
import android.util.Log
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import retrofit2.Call
import androidx.fragment.app.Fragment
import androidx.navigation.fragment.findNavController
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.funtech.amusementpark.models.Park
import com.funtech.amusementpark.services.Network
import retrofit2.Callback
import retrofit2.Response
import kotlin.collections.ArrayList

class ParkFragment : Fragment() {
    private var parks = ArrayList<Park>()
    private lateinit var linearLayoutManager: LinearLayoutManager
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: ParkRecyclerAdapter

    private fun getParks(offset: Int, limit: Int) {
        var parksCall : Call<List<Park>> = Network.parkService.getBatch(offset, limit)
        parksCall.enqueue(object : Callback<List<Park>> {
            override fun onResponse(call : Call<List<Park>>, response: Response<List<Park>>)
            {
                if (response.isSuccessful) {
                    for (park in response.body()!!) {
                        parks.add(park)
                    }
                    recyclerView.adapter?.notifyDataSetChanged()
                }
                else {
                    Log.e(TAG, "Failed to get parks from backend")
                }
            }

            override fun onFailure(call: Call<List<Park>>, t: Throwable) {
                Log.e(TAG, "Failed to get parks from backend")
            }
        })
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_park, container, false)
        val myActivity = activity as Activity
        myActivity.title = "PARKS"
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        adapter = ParkRecyclerAdapter(parks, view.context, findNavController())
        linearLayoutManager = LinearLayoutManager(activity, LinearLayoutManager.VERTICAL, false)
        recyclerView = view.findViewById(R.id.park_recycler_view) as RecyclerView
        recyclerView.adapter = adapter
        recyclerView.layoutManager = linearLayoutManager
        setRecyclerViewScrollListener(recyclerView)
        getParks(0, 5)
    }

    private fun setRecyclerViewScrollListener(recyclerView: RecyclerView) {
        recyclerView.addOnScrollListener(object : RecyclerView.OnScrollListener() {
            override fun onScrollStateChanged(recyclerView: RecyclerView, newState: Int) {
                super.onScrollStateChanged(recyclerView, newState)
                val totalItemCount = recyclerView.layoutManager!!.itemCount
                if (totalItemCount == linearLayoutManager.findLastVisibleItemPosition() + 1) {
                    getParks(totalItemCount, 5)
                }
            }
        })
    }


    companion object {
        private val TAG = "PARK_FRAGMENT"
        fun newInstance(): ParkFragment = ParkFragment()
    }
}