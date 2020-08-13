package com.funtech.amusementpark.services

import com.funtech.amusementpark.models.CreateUserRequest
import com.funtech.amusementpark.models.User
import retrofit2.Call
import retrofit2.http.*

interface UserService {
    @GET("/funtech/v1/users")
    fun getUserByEmail(@Query("email") email: String): Call<User>

    @POST("/funtech/v1/users")
    fun createUser(@Body createUserRequest: CreateUserRequest): Call<User>

}
