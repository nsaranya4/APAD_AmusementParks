package com.funtech.amusementpark.models

data class CreateUserRequest (val name: String, val image_id: String, val email: String, val role: String)