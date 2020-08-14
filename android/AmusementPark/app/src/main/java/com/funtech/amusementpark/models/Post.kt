package com.funtech.amusementpark.models

data class Post(val id: String, val title: String, val image_id: String, val tags: List<String>,
                val description: String, val location: Location, val user: User, val park: Park)