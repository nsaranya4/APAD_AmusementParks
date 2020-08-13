package com.funtech.amusementpark.services

import com.funtech.amusementpark.models.CreatePostRequest
import com.funtech.amusementpark.models.Post
import com.funtech.amusementpark.models.User
import retrofit2.Call
import retrofit2.http.*

interface PostService {

    @GET("/funtech/v1/posts")
    fun getPostsForPark(@Query("park_id") parkId: String,
                 @Query("offset") offset: Int,
                 @Query("limit") limit: Int): Call<List<Post>>

    @GET("/funtech/v1/posts")
    fun getPostsForUser(@Query("user_id") userId: String,
                        @Query("offset") offset: Int,
                        @Query("limit") limit: Int): Call<List<Post>>

    @GET("/funtech/v1/posts")
    fun getPostsByTag(@Query("tag") tag: String,
                        @Query("offset") offset: Int,
                        @Query("limit") limit: Int): Call<List<Post>>

    @GET("/funtech/v1/posts/{id}")
    fun getPostById(@Path("id") id: String): Call<Post>

    @POST("/funtech/v1/posts")
    fun createPost(@Body createPostRequest: CreatePostRequest): Call<Post>

}