<?php
session_start();
// Database connection details
$host = "localhost";
$username = "root";
$password = ""; // Replace with your MySQL password
$dbname = "login_database"; // Replace with your database name

// Create connection

$mysqli = new mysqli(hostname: $host,
                     username: $username,
                     password: $password,
                     database: $dbname);
                     
if ($mysqli->connect_errno) {
    die("Connection error: " . $mysqli->connect_error);
}

return $mysqli;




// $conn = mysqli_connect($servername, $username, $password, $dbname);


//  if (!$conn) {
//     die("COnnection Failed :" . mysqli_connect_error());
//  }

//  return $conn;
