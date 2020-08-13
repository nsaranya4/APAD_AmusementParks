package com.funtech.amusementpark.models

data class CreatePostRequest(val title: String, val image_id: String, val tags: List<String>,
                val description: String, val location: Location, val user_id: String, val park_id: String)