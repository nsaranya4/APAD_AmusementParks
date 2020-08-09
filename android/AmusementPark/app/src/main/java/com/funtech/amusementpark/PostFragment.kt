package com.funtech.amusementpark

import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.funtech.amusementpark.models.Post
import com.funtech.amusementpark.services.Network
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class PostFragment : Fragment() {
    private var posts = ArrayList<Post>()
    private var parkId = ""
    private lateinit var linearLayoutManager: LinearLayoutManager
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: PostRecyclerAdapter

        private fun getPostsForPark(parkId: String, offset: Int, limit: Int) {
        var postsCall : Call<List<Post>> = Network.postService.getPostsForPark(parkId, offset, limit)
            postsCall.enqueue(object : Callback<List<Post>> {
            override fun onResponse(call : Call<List<Post>>, response: Response<List<Post>>)
            {
                if (response.isSuccessful) {
                    for (post in response.body()!!) {
                        posts.add(post)
                    }
                    recyclerView.adapter?.notifyDataSetChanged()
                }
                else {
                    Log.e("PostRecycler", "Failed to get post from backend")
                }
            }

            override fun onFailure(call: Call<List<Post>>, t: Throwable) {
                Log.e("PostRecycler", "Failed to get post from backend")
            }
        })
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_post, container, false)
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        adapter = PostRecyclerAdapter(posts, view.context)
        linearLayoutManager = LinearLayoutManager(activity, LinearLayoutManager.VERTICAL, false)
        recyclerView = view.findViewById(R.id.post_recycler_view) as RecyclerView
        recyclerView.adapter = adapter
        recyclerView.layoutManager = linearLayoutManager
        setRecyclerViewScrollListener(recyclerView)
        getPostsForPark(parkId,0, 5)
    }

    private fun setRecyclerViewScrollListener(recyclerView: RecyclerView) {
        recyclerView.addOnScrollListener(object : RecyclerView.OnScrollListener() {
            override fun onScrollStateChanged(recyclerView: RecyclerView, newState: Int) {
                super.onScrollStateChanged(recyclerView, newState)
                val totalItemCount = recyclerView.layoutManager!!.itemCount
                if (totalItemCount == linearLayoutManager.findLastVisibleItemPosition() + 1) {
                    getPostsForPark(parkId, totalItemCount, 5)
                }
            }
        })
    }


    companion object {
        fun newInstance(): PostFragment = PostFragment()
    }
}