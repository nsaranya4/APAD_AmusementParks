package com.funtech.amusementpark.services

import com.funtech.amusementpark.models.User
import retrofit2.Call
import retrofit2.http.GET
import retrofit2.http.Query

interface UserService {
    @GET("/funtech/v1/users")
    fun getUserByEmail(@Query("email") email: String): Call<User>
}