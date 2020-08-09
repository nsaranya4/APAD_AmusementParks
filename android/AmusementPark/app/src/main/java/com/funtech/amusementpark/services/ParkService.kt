package com.funtech.amusementpark.services

import com.funtech.amusementpark.models.Park
import retrofit2.http.GET
import retrofit2.http.Query
import retrofit2.Call

interface ParkService {
    @GET("/funtech/v1/parks")
    fun getBatch(@Query("offset") offset: Int, @Query("limit") limit: Int): Call<List<Park>>
}