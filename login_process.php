<?php
session_start();

$isvalid = false;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $mysqli =require __DIR__ . "/db_connection.php";
    $sql = sprintf("SELECT password FROM users
                WHERE username = '%s'", $mysqli ->real_escape_string( $_POST["username"]));
    
    $result = $mysqli -> query($sql);
    
    $user = $result ->fetch_assoc();
    
     
    if (password_verify($_POST["password"], $user["password"])) {
        // Successful login, redirect to dashboard or other page
        $_SESSION['logged_in'] = true;
        header("location: welcome.php");
        exit;
    } else {
        // Handle login failure, e.g., display error message or redirect back to login page
        $_SESSION['message'] = "Invalid Login, Try again";
        header('Location: index.php');
        exit;
    }
}

