<?php
include "db_connection.php"
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="style.css">
    <title>Login Page</title>
</head>
<body>
    <div class="login-container">
        <h1>Login</h1>
        <?php 
        if(isset($_SESSION['message'])){
            $error = $_SESSION['message'];
        echo '<span style="color:red">'.$error.'</span>';
            session_destroy();
         }        
        ?>

        <form action="login_process.php" method="post">
            <label for="username">Username:</label>
            <input type="text" id="username" name="username" required>
            <label for="password">Password:</label>
            <input type="password" id="password" name="password" required>
            <button type="submit">Login</button>
            <p>Don't have an account? <a href="signup.php">Sign Up</a></p>
        </form>
    </div>
</body>
</html>