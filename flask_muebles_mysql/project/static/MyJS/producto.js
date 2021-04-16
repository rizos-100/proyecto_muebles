var categorias = [];
var materiales = [];
var materialesPro = [];
var productoInsertado = 0;

function llenarCategorias(){
    $.ajax(
        {
            type: "GET",
            url: "/getSelectCategorias",
            async: true
        })
        .done(
            function (data) {
                categorias = data;
                console.log(categorias)
                var str = '<option value="-1" selected disabled>-- Seleccion una categoria --</option>';
                for(var i = 0; i < categorias.length; i++){
                    str += '<option value="'+i+'">'+categorias[i].nombre+'</option>'
                }
                $('#lstCategoriasP').html(str);
            }
        );
}

function decidirProducto() {
    if ($('#txtIdProducto').val() == "") {
        agregarProducto();
    } else {
        modificarProducto();
    }
}

function seleccionarProducto(idP) {
    var data = {
        idProducto: idC
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllProductosById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                Producto = data;
                swal({
                    title: "¿Deseas continuar?",
                    text: "Por favor, confirma que deseas agregar el Producto a la venta.",
                    type: "info",
                    showCancelButton: true,
                    cancelButtonText: 'Cancelar',
                    confirmButtonColor: "#4caf50",
                    confirmButtonText: "Si, agregar",
                    closeOnConfirm: false,
                    showLoaderOnConfirm: false
                }, function () {
                    swal("Correcto", "Producto agregado a la venta. ", "success");
                    $('#txtNombreProductoVenta').text(Producto.persona.nombre + ' ' + Producto.persona.apellidoP + ' ' + Producto.persona.apellidoM);
                    $('#txtIdProductoAV').val(Producto.idProducto);
                    $('#modalProductoV').modal('hide');
                });

            }
        );

}

function cargarFoto() {
			var fileChooser = document.getElementById("txtFoto");
			var foto = document.getElementById("imgFoto");
			var base64 = document.getElementById("txtBase64");
			if (fileChooser.files.length > 0) {
				var fr = new FileReader();
				fr.onload = function () {
					foto.src = fr.result;
					base64.value = foto.src.replace
							(/^data:image\/(png|jpg|jpeg|gif);base64,/, '');
				}
				fr.readAsDataURL(fileChooser.files[0]);
			}
		}

function agregarProducto() {
    var err = validarProducto();
    if (err == "ok") {
        var data = {
            modelo:$('#txtModeloP').val(),
            alto:$('#txtAltoP').val(),
            color:$('#txtColorP').val(),
            largo:$('#txtLargoP').val(),
            ancho:$('#txtAnchoP').val(),
            peso:$('#txtPesoP').val(),
            cantidad:0,
            cantidad_minima:$('#txtCantidadMinimaP').val(),
            precio:$('#txtPrecioP').val(),
            img:'data:;base64,'+$('#txtBase64').val(),
            descripcion:$('#txtDescProducto').val(),
            idCategoria:categorias[$('#lstCategoriasP').val()].id

        };
        //console.log(data);
        swal({
            title: "¿Deseas continuar?",
            text: "Por favor, confirma que deseas agregar el registro.",
            type: "info",
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            confirmButtonColor: "#4caf50",
            confirmButtonText: "Si, agregar",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $.ajax(
                {
                    type: "POST",
                    url: "/addProducto",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        productoInsertado = data.id
                        swal("Correcto", "Producto guardado con exíto. ", "success");
                        $('#modalAgregarProductos').modal('hide');
                        setTimeout(function () {mostrarDetalleProductoMaterial(productoInsertado.id, 1);}, 2000)
                        
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function modificarProducto() {
    var err = validarProducto();
    if (err == "ok") {
        var data = {
            modelo:$('#txtModeloP').val(),
            alto:$('#txtAltoP').val(),
            color:$('#txtColorP').val(),
            largo:$('#txtLargoP').val(),
            ancho:$('#txtAnchoP').val(),
            peso:$('#txtPesoP').val(),
            cantidad:0,
            cantidad_minima:$('#txtCantidadMinimaP').val(),
            precio:$('#txtPrecioP').val(),
            img:'data:;base64,'+$('#txtBase64').val(),
            descripcion:$('#txtDescProducto').val(),
            idCategoria:categorias[$('#lstCategoriasP').val()].id,
            idProducto:$('#txtIdProducto').val()

        };
        //console.log(data);
        swal({
            title: "¿Deseas continuar?",
            text: "Por favor, confirma que deseas agregar el registro.",
            type: "info",
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            confirmButtonColor: "#4caf50",
            confirmButtonText: "Si, modificar",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $.ajax(
                {
                    type: "POST",
                    url: "/updateProducto",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        productoInsertado = data.id
                        swal("Correcto", "Producto modificado con exíto. ", "success");
                        $('#modalAgregarProductos').modal('hide');
                        setTimeout(function () {location.href = "/getAllProductosInactivos";}, 2000)
                        
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}


function guardarMaterialP() {
    var err = validarProductoMaterial();
    if (err == "ok") {
        var data = {
            alto:$('#txtAltoMate').val(),
            ancho:$('#txtAnchoMate').val(),
            cantidad:$('#txtCantidadMate').val(),
            idProducto:$('#txtIdProductoMa').val(),
            idMaterial:materiales[$('#lstMaterialMate').val()].id

        };
        //console.log(data);
        swal({
            title: "¿Deseas continuar?",
            text: "Por favor, confirma que deseas agregar el material, este registro no se podra modificar.",
            type: "info",
            showCancelButton: true,
            cancelButtonText: 'Cancelar',
            confirmButtonColor: "#4caf50",
            confirmButtonText: "Si, agregar",
            closeOnConfirm: false,
            showLoaderOnConfirm: true
        }, function () {
            $.ajax(
                {
                    type: "POST",
                    url: "/addDetalleProductosMaterial",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal("Correcto", "Material agregado con exíto. ", "success");
                        reiniciarProductoMaterial($('#txtIdProductoMa').val());
                        $('#txtIdDetalleProductoMa').val(data.id);
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function mostrarDetalleProductoMaterial(idP, mode){
    if(mode == 1){
        llenarListaMateriales();
        $('#lstMaterialDiv').show();
        $('#cantidadUsadaDiv').show();
        $('#txtIdProductoMa').val(idP);
        llenarMaterialesProducto(idP);
    }else{
        $('#txtIdProductoMa').val(idP);
        llenarMaterialesProducto(idP);
    }
    $('#modalDetalleProductoMaterial').modal('show');
}

function tipoMaterial(){
    if(materiales[$('#lstMaterialMate').val()].tipo == "Tabla"){
        $('#divAltoAnchoMate').show();
        $('#divBotones').show();
    }else{
        $('#divBotones').show();
    }
}

function reiniciarPagina(){
    console.log($('#txtIdDetalleProductoMa').val());
    if($('#txtIdDetalleProductoMa').val() != 0){
        setTimeout(function () { location.href = "/getAllProductosActivos"; }, 2000)
    }
}

function reiniciarProductoMaterial(){
    llenarMaterialesProducto($('#txtIdProductoMa').val());
    $('#divAltoAnchoMate').hide();
    $('#divBotones').hide();
}

function llenarMaterialesProducto(idP){
    var data = {
        idProducto: idP
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllDetalleProductosMaterial",
            async: true,
            data: data
        })
        .done(
            function (data) {
                materialesPro = data;
                $("#tbDetalleMaterialProducto > tbody").empty();
                var str="";
                console.log(materialesPro)
                for (var i = 0; i < materialesPro.length; i++) {
                    if(materialesPro[i].material.tipo == 'Tabla'){
                        str = '<tr><td><b>' + materialesPro[i].material.nombre + ' </b> <br><b>Alto usado: </b>' + materialesPro[i].alto + ' m <br><b>Ancho usado: </b>' + materialesPro[i].ancho + ' m</td><td>' + materialesPro[i].cantidad + '</td></tr>'
                    }
                    if(materialesPro[i].material.tipo != 'Tabla'){
                        str = '<tr><td><b>' + materialesPro[i].material.nombre + ' </b><br>';
                        if(materialesPro[i].material.tipo == 'Pintura'){
                            str += '<b>Color: </b>' + materialesPro[i].material.color + ' m';
                        }
                        str += '</td><td class="text-centers">' + materialesPro[i].cantidad + '</td></tr>';
                    }
                }
                if(materialesPro.length <= 0){
                    str += '<tr><td class="text-center" colspan="2">No se encontraron materiales de este producto</td></tr>';
                }
                $('#tbodyDetalleMaterialProducto').html(str);
            }
        );
}

function llenarListaMateriales(){
    $.ajax(
        {
            type: "GET",
            url: "/getSelectMateriales",
            async: true
        })
        .done(
            function (data) {
                materiales = data;
                console.log(materiales)
                var str = '<option value="-1" selected disabled>-- Seleccion una categoria --</option>';
                for(var i = 0; i < materiales.length; i++){
                    str += '<option value="'+i+'">'+materiales[i].nombre+' '+materiales[i].tipo +'</option>'
                }
                $('#lstMaterialMate').html(str);
            }
        );
}

function validarProducto() {
    if ($('#txtModelP').val() == "") {
        return "Por favor, indica el modelo. ";
    }
    if ($('#txtColorP').val() == "") {
        return "Por favor, indica el color. ";;
    }
    if ($('#txtAltoP').val() == "") {
        return "Por favor, indica el alto. ";;
    }
    if ($('#txtLargoP').val() == "") {
        return "Por favor, indica el largo. ";
    }
    if ($('#txtAnchoP').val() == "") {
        return "Por favor, indica el ancho. ";
    }
    if ($('#txtPesoP').val() == "") {
        return "Por favor, indica el peso. ";
    }
    if ($('#txtCantidadMinimaP').val() == "") {
        return "Por favor, indica la cantidad minima. ";
    }
    if ($('#txtPrecioP').val() == "") {
        return "Por favor, indica el precio. ";
    }
    if ($('#txtBase64').val() == "") {
        return "Por favor, selecciona una imagen para el producto. ";
    }
    if ($('#txtDescProducto').val() == "") {
        return "Por favor, indica la descripción del producto. ";
    }
    if ($('#lstCategoriasP').val() == -1) {
        return "Por favor, indica la categoria. ";
    }
    

    return "ok";
}

function validarProductoMaterial() {
    if(materiales[$('#lstMaterialMate').val()].tipo == "Tabla"){
        if ($('#txtCantidadMate').val() == "") {
            return "Por favor, indica la cantidad. ";;
        }
        if ($('#txtAltoMate').val() == "") {
            return "Por favor, indica el alto. ";;
        }
        if ($('#txtAnchoMate').val() == "") {
            return "Por favor, indica el ancho. ";
        }
        if ($('#lstMaterialMate').val() == null) {
            return "Por favor, indica el material. ";
        }
    }else{
        if ($('#txtCantidadMate').val() == "") {
            return "Por favor, indica la cantidad. ";;
        }
        if ($('#lstMaterialMate').val() == null) {
            return "Por favor, indica el material. ";
        }
    }
    
    

    return "ok";
}

function mostrarProductos(idP){
    limpiarModalProductor();
    var data = {
        id: idP
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllProductosPorId",
            async: true,
            data: data
        })
        .done(
            function (data) {
                producto = data[0];

                var str = '<option value="-1" disabled>-- Seleccion una categoria --</option>';
                for(var i = 0; i < categorias.length; i++){
                    if(categorias[i].id == producto.categoria.id){
                        str += '<option value="'+i+'" selected>'+categorias[i].nombre+'</option>'
                    }else{
                        str += '<option value="'+i+'">'+categorias[i].nombre+'</option>'
                    }
                }
                $('#lstCategoriasP').html(str);
                $('#txtIdProducto').val(producto.idProducto);
                $('#txtModeloP').val(producto.modelo);
                $('#txtColorP').val(producto.color);
                $('#txtAltoP').val(producto.alto);
                $('#txtLargoP').val(producto.largo);
                $('#txtAnchoP').val(producto.ancho);
                $('#txtPesoP').val(producto.peso);
                $('#txtCantidadMinimaP').val(producto.cantidad_minima);
                $('#txtPrecioP').val(producto.precio);
                $('#imgFoto').attr("src",producto.img);
                $('#txtBase64').val(producto.img);
                $('#txtDescProducto').val(producto.descripcion);
                $('#modalAgregarProductos').modal('show');
            }
        );
}

function eliminarProducto(idP) {
    var data = {
        idVenta: idP
    };
    swal({
        title: "¿Deseas continuar?",
        text: "Por favor, confirma que deseas eliminar el registro.",
        type: "info",
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Si, eliminar",
        closeOnConfirm: false,
        showLoaderOnConfirm: true
    }, function () {
        $.ajax(
            {
                type: "POST",
                url: "/deleteProducto",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Producto eliminado con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllProductosInactivos"; }, 2000)
                }
            );
    });

}

function limpiarModalProductor() {
    llenarCategorias();

    $('#txtIdProducto').val("");
    $('#txtModeloP').val("");
    $('#txtColorP').val("");
    $('#txtAltoP').val("");
    $('#txtLargoP').val("");
    $('#txtAnchoP').val("");
    $('#txtPesoP').val("");
    $('#txtCantidadMinimaP').val("");
    $('#txtPrecioP').val("");
    $('#txtBase64').val("");
    $('#txtDescProducto').val("");
}

/* Funciones para notificaciones */

function showNotification(colorName, text, placementFrom, placementAlign, animateEnter, animateExit) {
    if (colorName === null || colorName === '') {
        colorName = 'bg-black';
    }
    if (text === null || text === '') {
        text = 'Turning standard Bootstrap alerts';
    }
    if (animateEnter === null || animateEnter === '') {
        animateEnter = 'animated fadeInDown';
    }
    if (animateExit === null || animateExit === '') {
        animateExit = 'animated fadeOutUp';
    }
    var allowDismiss = true;

    $.notify({
        message: text
    },
        {
            type: colorName,
            allow_dismiss: allowDismiss,
            newest_on_top: true,
            timer: 1000,
            z_index: 1500,
            placement: {
                from: placementFrom,
                align: placementAlign
            },
            animate: {
                enter: animateEnter,
                exit: animateExit
            },
            template: '<div data-notify="container" class="bootstrap-notify-container alert alert-dismissible {0} ' + (allowDismiss ? "p-r-35" : "") + '" role="alert">' +
                '<button type="button" aria-hidden="true" class="close" data-notify="dismiss">×</button>' +
                '<span data-notify="icon"></span> ' +
                '<span data-notify="title">{1}</span> ' +
                '<span data-notify="message">{2}</span>' +
                '<div class="progress" data-notify="progressbar">' +
                '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
                '</div>' +
                '<a href="{3}" target="{4}" data-notify="url"></a>' +
                '</div>'
        });
}