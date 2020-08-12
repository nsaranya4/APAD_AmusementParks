package com.funtech.amusementpark.models

data class CreatePostRequest(val title: String, val image_id: String,
                val description: String, val location: Location, val user: User, val park: Park)