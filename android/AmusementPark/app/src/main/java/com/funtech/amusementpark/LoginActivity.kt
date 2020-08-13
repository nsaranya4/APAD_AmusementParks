package com.funtech.amusementpark

import android.content.Context
import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.ProgressBar
import android.widget.Toast
import androidx.annotation.StringRes
import androidx.appcompat.app.AppCompatActivity
import com.funtech.amusementpark.models.CreateUserRequest
import com.funtech.amusementpark.models.User
import com.funtech.amusementpark.services.Network
import com.google.android.gms.auth.api.signin.GoogleSignIn
import com.google.android.gms.auth.api.signin.GoogleSignInClient
import com.google.android.gms.auth.api.signin.GoogleSignInOptions
import com.google.android.gms.common.api.ApiException
import com.google.firebase.auth.FirebaseAuth
import com.google.firebase.auth.FirebaseUser
import com.google.firebase.auth.GoogleAuthProvider
import com.google.firebase.auth.ktx.auth
import com.google.firebase.ktx.Firebase
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response


class LoginActivity : AppCompatActivity() {
    private lateinit var loginButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var googleSignInClient: GoogleSignInClient
    private lateinit var auth: FirebaseAuth


    private fun showLoginFailed() {
        Toast.makeText(applicationContext, "Login Failed", Toast.LENGTH_SHORT).show()
    }

    private fun startMainActivity(context: Context) {
        var intent = Intent(context, MainActivity::class.java)
        startActivity(intent)
    }

    private fun storeUserInSharePreferences(user: User) {
        var sharedPreferences = getSharedPreferences("funtech", Context.MODE_PRIVATE);
        val editor = sharedPreferences.edit()
        editor.putString("user_id", user.id)
        editor.putString("user_email", user.email)
        editor.putString("user_name", user.name)
        editor.commit()
    }

    private fun createUser(context: Context, createUserRequest: CreateUserRequest) {
        var userCall : Call<User> = Network.userService.createUser(createUserRequest)
        userCall.enqueue(object : Callback<User> {
            override fun onResponse(call : Call<User>, response: Response<User>)
            {
                if (response.isSuccessful) {
                    val user = response.body()!!
                    storeUserInSharePreferences(user)
                    progressBar.visibility = View.GONE
                    startMainActivity(context)
                }
                else {
                    Log.e(TAG, "Failed to creates user in the backend")
                }
            }

            override fun onFailure(call: Call<User>, t: Throwable) {
                Log.e(TAG, "Failed to creates user in the backend")
            }
        })
    }

    private fun createUserIfNotExist(context: Context, user: FirebaseUser) {
        var userCall : Call<User> = Network.userService.getUserByEmail(user.email!!)
        userCall.enqueue(object : Callback<User> {

            override fun onResponse(call : Call<User>, response: Response<User>)
            {
                if (response.isSuccessful) {
                    val user = response.body()!!
                    storeUserInSharePreferences(user)
                    progressBar.visibility = View.GONE
                    startMainActivity(context)
                } else if (response.code() == 404) {
                    Log.d(TAG, "Creating new user")
                    val createUserRequest = CreateUserRequest(user.displayName!!, "image_id", user.email!!, "admin")
                    createUser(context, createUserRequest)
                } else {
                    Log.e(TAG, "Failed to get user by email from backend")
                    showLoginFailed()
                }
            }

            override fun onFailure(call: Call<User>, t: Throwable) {
                Log.e(TAG, "Failed to get user by email from backend")
                showLoginFailed()
            }
        })
    }

    private fun firebaseAuthWithGoogle(context: Context, idToken: String) {
        val credential = GoogleAuthProvider.getCredential(idToken, null)
        auth.signInWithCredential(credential)
            .addOnCompleteListener(this) { task ->
                if (task.isSuccessful) {
                    Log.d(TAG, "signInWithCredential:success")
                    createUserIfNotExist(context, auth.currentUser!!)
                } else {
                    Log.w(TAG, "signInWithCredential:failure", task.exception)
                    showLoginFailed()
                }
            }
    }

    private fun signIn() {
        val signInIntent = googleSignInClient.signInIntent
        progressBar.visibility = View.VISIBLE
        startActivityForResult(signInIntent, RC_SIGN_IN)
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        Log.d(TAG, "Oncreate")
        setContentView(R.layout.activity_login)
        Log.d(TAG, "Login activity on create")


        val gso = GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
            .requestIdToken(getString(R.string.default_web_client_id))
            .requestEmail()
            .build()

        googleSignInClient = GoogleSignIn.getClient(this, gso)
        auth = Firebase.auth
        loginButton = findViewById<Button>(R.id.login);
        progressBar = findViewById<ProgressBar>(R.id.loading)
        Log.d(TAG, "login button onclick listener set")
        loginButton.setOnClickListener {
            Log.d(TAG, "login button clicked")
            loginButton.visibility = View.GONE
            signIn()
        }

    }
    
    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        if (requestCode == RC_SIGN_IN) {
            Log.d(TAG, "Google signin result")
            val task = GoogleSignIn.getSignedInAccountFromIntent(data)
            try {
                val account = task.getResult(ApiException::class.java)!!
                Log.d(TAG, "firebaseAuthWithGoogle:" + account.id)
                firebaseAuthWithGoogle(this, account.idToken!!)
            } catch (e: ApiException) {
                Log.w(TAG, "Google sign in failed", e)
            }
        }
    }

    companion object {
        private const val TAG = "LOGIN_ACTIVITY"
        private const val RC_SIGN_IN = 9001
    }
}