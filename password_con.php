<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Change</title>
    <link rel="stylesheet" href="ps_style.css">
</head>
<body>
    <div class="container">
        <h1>Change Password</h1>
        <form action="#">
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" name="username" required placeholder="Enter your username">
            </div>
            <div class="form-group">
                <label for="newPassword">New Password:</label>
                <input type="password" id="newPassword" name="newPassword" required placeholder="new password">
            </div>
            <div class="form-group">
                <label for="ConfirmPassword">Confirm Password:</label>
                <input type="password" id="confirmPassword" name="confirmPassword" required placeholder="Confirm Password">
            </div>
            <button type="submit">Change Password</button>
        </form>
    </div>
</body>
</html>