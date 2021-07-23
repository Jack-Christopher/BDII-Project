<html>
<head>
    <meta charset="UTF-8">
    <title>Tienda XYZ</title>

    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css"> 
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script>
    
    
    <link rel="stylesheet" href="../CSS_Files/index.css">
    <link rel="shortcut icon" href="../../Images/icon.jpg" type="image/jpg">
    
<title> Únete a Tienda XYZ </title>
<link rel="stylesheet" href="../CSS_Files/register.css">

</head>

<body >

    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
  
        <div class="collapse navbar-collapse" id="navbar">
          <div class="navbar-nav">
              <a class="nav-link active" href="../HTML_Files/index.html">Inicio</a>
              <a class="nav-link" href="#">ABCD</a>
              <a class="nav-link" href="#">DEFG</a>
              <a class="nav-link" href="#">HIJK</a>
          </div>
        </div>
      </div>
  
    </nav>


    <button type="button" class="btn btn-success" id="addProduct">+ Agregar Producto</button>

    <div class="modal fade" id="myModal" role="dialog">
        <div class="modal-dialog">
        
          <!-- Modal content-->
          <div class="modal-content">
            <div class="modal-header">
                <h4 class="modal-title">Agregar Producto</h4>
                <button type="button" class="close" data-dismiss="modal">&times;</button>
            </div>
            
            <div class="modal-body">
              <p>here goes the code</p>
            </div>

            <div class="modal-footer">
              <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>
            </div>
          </div>
          
        </div>
      </div>


              
    </div>

    <script>
        $(document).ready(function(){
          $("#addProduct").click(function(){
            $("#myModal").modal({backdrop: true});
          });
        });
    </script>
      
</body>
</html>