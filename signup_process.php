<?php
     
     //include "db_connection.php";
if ($_SERVER["REQUEST_METHOD"] == "POST") {
     if (empty($_POST["username"])) {
        die("Name is required");
    }
    
    if ( ! filter_var($_POST["email"], FILTER_VALIDATE_EMAIL)) {
        die("Valid email is required");
    }
    
    if (strlen($_POST["password"]) < 8) {
        die("Password must be at least 8 characters");
    }
    
    if ( ! preg_match("/[a-z]/i", $_POST["password"])) {
        die("Password must contain at least one letter");
    }
    
    if ( ! preg_match("/[0-9]/", $_POST["password"])) {
        die("Password must contain at least one number");
    }
    
    if ($_POST["password"] !== $_POST["cpassword"]) {
        die("Passwords must match");
    }
  
    
    $mysqli = require __DIR__ . "/db_connection.php";
    
    $sql = "INSERT INTO users(username,email,password)
            VALUES (?, ?, ?)";
            
    $stmt = $mysqli->stmt_init();
    
    if ( ! $stmt->prepare($sql)) {
        die("SQL error: " . $mysqli->error);
    }
      
    $password = password_hash($_POST["password"], PASSWORD_DEFAULT);
    $stmt->bind_param("sss",
    $_POST["username"],
    $_POST["email"],
    //$password
    $password);
                      
    if ($stmt->execute()) {
    
        header("Location: index.php");
        exit;
        
    } else {
        
        if ($mysqli->errno === 1062) {
            die("email already taken");
        } else {
            die($mysqli->error . " " . $mysqli->errno);
        }
    }

}


















    //  if (isset($_POST['submit'])) {
    //     $username = filter_var($_POST['username'], FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    //     $email = filter_var($_POST['email'], FILTER_SANITIZE_EMAIL);
    //     $password = filter_var($_POST['password'],FILTER_SANITIZE_FULL_SPECIAL_CHARS);
    //     $cpassword = filter_var($_POST['cpassword'],FILTER_SANITIZE_FULL_SPECIAL_CHARS);


    //     // echo "$username $email $password $cpassword";

        
        
    //     $sql = "Select * from user_details where username='$username'";
    //     $result = mysqli_query($conn, $sql);        
    //     $count_user = mysqli_num_rows($result);  
        
        

        
    //     if($count_user == 0){  
    //         if ($password == $cpassword){
    //             $hash = password_hash($password, PASSWORD_DEFAULT);
                    
    //             echo 'successful';
    //             // Password Hashing is used here. 
    //             $sql = "INSERT INTO user_details(username, password, cpassword) VALUES('$username', '$hash','$cpassword')";
        

    //             $result = mysqli_query($conn, $sql);
        
    //             if(!mysqli_errno($conn)){
                
    //                 // header('location: ' . 'welcome.php');
    //                 // die();
    //             }
    //         } else {
    //             echo 'error';
    //         }

          
    //     }     
    // }