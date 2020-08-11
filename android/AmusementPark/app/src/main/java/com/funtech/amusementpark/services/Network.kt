package com.funtech.amusementpark.services

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

object Network {
    val retrofit = Retrofit.Builder()
        .baseUrl("https://funtech-backend.uc.r.appspot.com")
        .addConverterFactory(GsonConverterFactory.create())
        .build()
    val parkService = retrofit.create(ParkService::class.java)
    val postService = retrofit.create(PostService::class.java)
    val userService = retrofit.create(UserService::class.java)
}