package com.funtech.amusementpark

import android.app.Activity
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import android.widget.Button
import android.widget.ProgressBar
import androidx.navigation.fragment.findNavController
import androidx.navigation.fragment.navArgs
import androidx.recyclerview.widget.LinearLayoutManager
import androidx.recyclerview.widget.RecyclerView
import com.funtech.amusementpark.models.Post
import com.funtech.amusementpark.services.Network
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class PostFragment : Fragment() {
    private var posts = ArrayList<Post>()
    private lateinit var parkId: String
    private lateinit var linearLayoutManager: LinearLayoutManager
    private lateinit var recyclerView: RecyclerView
    private lateinit var adapter: PostRecyclerAdapter
    val args: PostFragmentArgs by navArgs()

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
                    Log.e(TAG, "Failed to get posts from backend")
                }
            }

            override fun onFailure(call: Call<List<Post>>, t: Throwable) {
                Log.e(TAG, "Failed to get posts from backend")
            }
        })
    }

    private fun openCreatePostFragment() {
        val action = PostFragmentDirections.actionPostFragmentToCreatePostFragment(this.parkId)
        findNavController().navigate(action)
    }

    override fun onCreateView(
        inflater: LayoutInflater,
        container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        val view = inflater.inflate(R.layout.fragment_post, container, false)
        val myActivity = activity as Activity
        myActivity.title = "POSTS"
        return view
    }

    override fun onViewCreated(view: View, savedInstanceState: Bundle?) {
        super.onViewCreated(view, savedInstanceState)
        parkId = args.parkId
        val createPostButton = view.findViewById(R.id.create_post) as Button
        createPostButton.setOnClickListener {
            Log.d(TAG, "create post button clicked")
            openCreatePostFragment()
        }
        adapter = PostRecyclerAdapter(posts, view.context, findNavController())
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
        private val TAG = "POST_FRAGMENT"
        fun newInstance(): PostFragment = PostFragment()
    }
}