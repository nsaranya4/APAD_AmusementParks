package com.funtech.amusementpark

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import com.funtech.amusementpark.models.Post
import com.funtech.amusementpark.models.User
import com.funtech.amusementpark.services.Network
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response

class SinglePostFragment : Fragment() {

    private fun getPostById(context: Context, id: String) {
        var postCall : Call<Post> = Network.postService.getPostById(id)
        postCall.enqueue(object : Callback<Post> {
            override fun onResponse(call : Call<Post>, response: Response<Post>)
            {
                if (response.isSuccessful) {
                    val post = response.body()!!

                }
                else {
                    Log.e(TAG, "Fail to get post by id")

                }
            }

            override fun onFailure(call: Call<Post>, t: Throwable) {
                Log.e(TAG, "Fail to get post by id")
            }
        })
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
    }

    override fun onCreateView(
        inflater: LayoutInflater, container: ViewGroup?,
        savedInstanceState: Bundle?
    ): View? {
        // Inflate the layout for this fragment
        return inflater.inflate(R.layout.fragment_single_post, container, false)
    }

    companion object {
        private val TAG = "SINGLE_POST_FRAGMENT"
        fun newInstance(): SinglePostFragment = SinglePostFragment()
    }
}