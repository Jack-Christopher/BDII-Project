<html>
<head>
    <title> Bienvenido a Tienda XYZ </title>
    <link rel="stylesheet" href="../CSS_Files/login.css">

    <?php   include_once("include_important.php");  ?>

</head>

<body background="../../Images/blue_background.jpg"  style="background-size: cover"> 
   
<br><br>
    <div class="jumbotron" id="login_container"  style="background:#cfe7ff;">
        <div align="center" >
            <img src="../../Images/login_icon_2.png" alt="Icono de inicio de sesión" width="150" height="150"> 
        </div> 
        <br>

    <form id="login_form" >
        <label for="user_name"> Nombre de Usuario: </label>
        <input type="text" name="user_name" id="user_name" class="form-control">
        <label for="password"> Contraseña </label>
        <input type="password" name="password" id="password" class="form-control">

            <br> 
        
        <div align="right">
            <button type="button" id="submit_button" class="btn btn-primary" > Iniciar Sesión </button>
            
        </div>
    </form>
    <br>  ¿No tienes una cuenta? 
        <a href="../PHP_Files/register_page.php"> Regístrate </a>
        <br>
        <a href="../HTML_Files/main_view.html"> Unirse como invitado </a>
    </div>
</body>
</html>

<script>
    function formEsValido()
    {
        var nombre_de_usuario = $("#user_name");
        var clave_de_usuario = $("#password");

        if(nombre_de_usuario.val() == "")
        {
            var op = alertify.alert("Debe colocar su nombre de usuario.").setHeader("Atención");

            return false;
            
        }
        else if(clave_de_usuario.val() == "")
        {
            alertify.alert("Debe colocar su clave de usuario" ).setHeader("Atención");
            return false;
        }

        return true;
    }

    
    $(document).ready( function() 
    { 
        $("#submit_button").click( function() 
        {
            if(formEsValido())
            {
                // Aqui va la conexion a Cassandra                 
            }
            
        })
    })
</script>