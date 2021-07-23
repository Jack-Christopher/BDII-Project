<html>
<head>
<title> Únete a Tienda XYZ </title>
<link rel="stylesheet" href="../CSS_Files/register.css">
<?php   include_once("include_important.php");  ?>
</head>

<body background="../../Images/blue_background.jpg"  style="background-size: cover"> 

<br><br>
    <div class="jumbotron" id="signup_container" style="background:#cfe7ff; ">  <!-- c3f6c3 -->

    <form id="signup_form" >
        <label for="name"> Nombres: </label>
        <input type="text" name="name" id="name" class="form-control">
        <label for="last_name"> Apellidos: </label>
        <input type="text" name="last_name" id="last_name" class="form-control">
        <label for="e_mail"> Correo Electrónico: </label>
        <input type="email" name="e_mail" id="e_mail" class="form-control">
        <label for="cellphone"> Número de celular: </label>
        <input type="tel" name="cellphone" id="cellphone" class="form-control">
        <label for="client_DNI"> DNI del cliente: </label>
        <input type="text" name="client_DNI" id="client_DNI" class="form-control">
        <label for="password"> Contraseña </label>
        <input type="password" name="password" id="password" class="form-control">
        <label for="password_again"> Repite tu contraseña </label>
        <input type="password" name="password_again" id="password_again" class="form-control">

            <br> 
        
        <div align="right">
            <button type="button" id="submit_button" class="btn btn-success" > Registrarse </button>
        </div>
    
    </form>
    <br>  ¿Ya tienes una cuenta?
        <a href="../PHP_Files/start_sale.php"> Inicia Sesión </a>
    </div>
</body>
</html>









<script>
    function formEsValido()
    {
        var nombres = $("#name");
        var apellidos = $("#last_name");
        var correo_electronico = $("#e_mail");
        var numero_de_celular = $("#cellphone");
        var nombre_de_cliente = $("#client_DNI");
        var clave_de_cliente = $("#password");
        var clave_de_cliente2 = $("#password_again");

        if( nombres.val() == "")
        {
            var op = alertify.alert("Debe colocar sus nombres." );
            return false;
        }
        else if( apellidos.val() == "")
        {
            var op = alertify.alert("Debe colocar sus apellidos." );
            return false;
        }
        else if( correo_electronico.val() == "")
        {
            var op = alertify.alert("Debe colocar su correo electrónico." );
            return false;
        }
        else if( numero_de_celular.val() == "")
        {
            var op = alertify.alert("Debe colocar su numero de celular." );
            return false;
        }
        else if( nombre_de_cliente.val() == "")
        {
            var op = alertify.alert("Debe colocar su DNI del cliente.");
            return false;
        }
        else if( clave_de_cliente.val() == "")
        {
            var op = alertify.alert("Debe colocar su clave de cliente." );
            return false;
        }
        else if( clave_de_cliente2.val() == "")
        {
            var op = alertify.alert("Debe colocar su clave de cliente otra vez." );
            return false;
        }
        else if ( clave_de_cliente.val() != clave_de_cliente2.val())
        {
            var op = alertify.alert("Las clave de cliente deben coincidir." );
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
