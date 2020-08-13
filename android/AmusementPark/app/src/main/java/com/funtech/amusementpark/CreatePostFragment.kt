package com.funtech.amusementpark

import android.content.Context
import android.content.SharedPreferences
import android.os.Bundle
import android.util.Log
import androidx.fragment.app.Fragment
import android.view.LayoutInflater
import android.view.View
import android.view.ViewGroup
import androidx.navigation.fragment.navArgs
import com.funtech.amusementpark.models.CreatePostRequest
import com.funtech.amusementpark.models.Post
import com.funtech.amusementpark.services.Network
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class CreatePostFragment : Fragment() {
    private lateinit var parkId: String
    private lateinit var userId: String
    val args: PostFragmentArgs by navArgs()

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

    companion object {
        private val TAG = "CREATE_POST_FRAGMENT"
        fun newInstance(): CreatePostFragment = CreatePostFragment()
    }
}