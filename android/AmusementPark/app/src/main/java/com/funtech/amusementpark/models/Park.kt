package com.funtech.amusementpark.models

data class Park(val id: String, val name: String, val image_id: String,
                val description: String, val location: Location, val user: User)


