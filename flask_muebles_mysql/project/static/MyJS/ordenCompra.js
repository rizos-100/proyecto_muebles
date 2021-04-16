var proveedor = "";
materiales=[];

function ValidarCantidadSubtotal(){
    var cantidad_v = parseInt($('#txtCantidadMaterialOV').val());
    var subtotal_ = parseFloat($('#txtSubtotalMaterialOV').val());

    if(cantidad_v <= 0){
        showNotification("bg-red", "Por favor, ingresa una cantidad mayor a 0", "bottom", "right", "", "");
        return false;
    }

    if(subtotal_ <= 0){
        showNotification("bg-red", "Por favor, ingresa un subtotal mayor a 0", "bottom", "right", "", "");
        return flase;
    }

    $('#modalMaterialOV').modal('show');
}

function detalleOrden(idO) {
    var data = {
        idOrden: idO
    };
    $.ajax(
        {
            type: "POST",
            url: "/getAllOrdenCompraById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                ordenCompra = data;
                console.log(ordenCompra)
                $('#txtNombreProvOV').text(ordenCompra.proveedor.nombre);
                $('#txtNombreConProvOV').text(ordenCompra.proveedor.nombre_contacto);
                $('#txtTelCProvOV').text(ordenCompra.proveedor.telefono_contacto);
                $('#txtEmailConProvOV').text(ordenCompra.proveedor.correo_contacto);
                $('#txtEmpleadoOV').text(ordenCompra.user.nombre + ' ' + ordenCompra.user.apellidoP + ' ' + ordenCompra.user.apellidoM);
                $('#txtFechaOV').text(ordenCompra.fecha_orden);
                $('#txtTotalOV').text(ordenCompra.total);
                detalleMaterialOV = ordenCompra.materiales;
                $("#tbDetalleOV > tbody").empty();
                for (var i = 0; i < detalleMaterialOV.length; i++) {
                    $("#tbDetalleOV>tbody").append('<tr><td>' + detalleMaterialOV[i].tipo + '</td><td>' + detalleMaterialOV[i].material + '</td><td>' + detalleMaterialOV[i].cantidad + '</td><td>' + detalleMaterialOV[i].subtotal + '</td></tr>');
                }
                $('#modalDetalleOrdenCompra').modal('show');
            }
        );
}

function detalleOrdenAgregar(idO) {
    var data = {
        idOrden: idO
    };
    $.ajax(
        {
            type: "POST",
            url: "/getAllOrdenCompraById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                ordenCompra = data;
                console.log(ordenCompra)
                $('#txtNombreProvOVA').text(ordenCompra.proveedor.nombre);
                $('#txtNombreConProvOVA').text(ordenCompra.proveedor.nombre_contacto);
                $('#txtTelCProvOVA').text(ordenCompra.proveedor.telefono_contacto);
                $('#txtEmailConProvOVA').text(ordenCompra.proveedor.correo_contacto);
                $('#txtEmpleadoOVA').text(ordenCompra.user.nombre + ' ' + ordenCompra.user.apellidoP + ' ' + ordenCompra.user.apellidoM);
                $('#txtFechaOVA').text(ordenCompra.fecha_orden);
                $('#txtTotalOVA').text(ordenCompra.total);
                detalleMaterialOV = ordenCompra.materiales;
                $("#tbDetalleOVA > tbody").empty();
                for (var i = 0; i < detalleMaterialOV.length; i++) {
                    $("#tbDetalleOVA>tbody").append('<tr><td>' + detalleMaterialOV[i].tipo + '</td><td>' + detalleMaterialOV[i].material + '</td><td>' + detalleMaterialOV[i].cantidad + '</td><td>' + detalleMaterialOV[i].subtotal + '</td></tr>');
                }
                $('#modalDetalleOrdenCompraAgregar').modal('show');
            }
        );
}

function seleccionarProveedor(idP) {
    var data = {
        idProveedor: idP
    };
    $.ajax(
        {
            type: "POST",
            url: "/getAllProveedorById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                proveedor = data;
                swal({
                    title: "¿Deseas continuar?",
                    text: "Por favor, confirma que deseas agregar el proveedor a la orden de compra.",
                    type: "info",
                    showCancelButton: true,
                    cancelButtonText: 'Cancelar',
                    confirmButtonColor: "#4caf50",
                    confirmButtonText: "Si, agregar",
                    closeOnConfirm: false,
                    showLoaderOnConfirm: false
                }, function () {
                    swal("Correcto", "Proveedor agregado a la orden de compra. ", "success");
                    $('#txtNombrePOV').text(proveedor.nombre);
                    $('#modalProveedorOV').modal('hide');
                });

            }
        );

}

function seleccionarMaterial(idM) {

    var data = {
        id: idM
    };
    $.ajax(
        {
            type: "GET",
            url: "/getMateriaOrdenById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                material = data;
                console.log(data);
                swal({
                    title: "¿Deseas continuar?",
                    text: "Por favor, confirma que deseas agregar el material.",
                    type: "info",
                    showCancelButton: true,
                    cancelButtonText: 'Cancelar',
                    confirmButtonColor: "#4caf50",
                    confirmButtonText: "Si, agregar",
                    closeOnConfirm: false,
                    showLoaderOnConfirm: false
                }, function () {

                    var cantidad = parseInt($('#txtCantidadMaterialOV').val());
                    var subtotal = parseFloat($('#txtSubtotalMaterialOV').val());

                    var parametros_envio = {
                        "tipo": material.tipo,
                        "nombre": material.nombre,
                        "idMaterial": material.id,
                        "cantidad": cantidad,
                        "subtotal": subtotal
                    };
                    materiales.push(parametros_envio);
                    llenarTablaDetalleMaterialOrden();
                    $('#txtCantidadMaterialOV').val(1)
                    $('#txtSubtotalMaterialOV').val(1)
                    swal("Correcto", "Material agregado a la orden de compra. ", "success");
                    $('#modalMaterialOV').modal('hide');
                });
            }
        );
}

function eliminarMaterialOrden(indice) {
    swal({
        title: "¿Deseas continuar?",
        text: "Por favor, confirma que deseas eliminar el material de la orden de compra.",
        type: "info",
        showCancelButton: true,
        cancelButtonText: 'Cancelar',
        confirmButtonColor: "#DD6B55",
        confirmButtonText: "Si, eliminar",
        closeOnConfirm: false,
        showLoaderOnConfirm: false
    }, function () {
        materiales.splice(indice, 1);
        $('#txtCantidadMaterialOV').val(1)
        $('#txtSubtotalMaterialOV').val(1)
        swal("Correcto", "Material eliminado de la orden de compra. ", "success");
        llenarTablaDetalleMaterialOrden();
    });
}

function llenarTablaDetalleMaterialOrden() {
    var datos = "";
    var total = 0;
    if (materiales.length === 0) {
        datos += '<tr>';
        datos += '<td> No hay registros para mostrar</td>';
        datos += '<td> </td>';
        datos += '<td> </td>';
        datos += '<td> </td>';
        datos += '<td> </td>';
        datos += '</tr>';
        $('#tbodyOrdenAgregarMaterial').html(datos);
        $('#txtTotalOrdenAgregar').text("-");
        $('#txtCantidadMaterialOV').val(1)
        $('#txtSubtotalMaterialOV').val(1)
    } else {
        $("#tbOrdenAgregarMaterial > tbody").empty();
        for (var i = 0; i < materiales.length; i++) {
            total = total + parseFloat(materiales[i]["subtotal"]);
            //console.log(productos[i]["subtotal"]);
            $("#tbOrdenAgregarMaterial>tbody").append('<tr><td>' + materiales[i]["tipo"] + '</td><td>' + materiales[i]["nombre"] + '</td><td>' + materiales[i]["cantidad"] + '</td><td>' + materiales[i]["subtotal"] + '</td><td class="text-center"> <button type="button" class="btn btn-danger waves-effect" onclick="eliminarMaterialOrden(' + i + ')"> <i class="material-icons">delete</i></button> </td></tr>');
        }
        $('#txtTotalOrdenAgregar').text(total);
    }
}

function agregarOrdenCompra() {
    var err = validarOrden();
    if (err == "ok") {
        var data = {
            total: parseFloat($('#txtTotalOrdenAgregar').text()),
            idProveedor: proveedor.id,
            idUser: localStorage.getItem("idUser"),
            materiales_orden: JSON.stringify(materiales)
        };
        console.log(data);
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
                    url: "/addOrdenCompra",
                    async: true,
                    data: data
                })
                .done(
                    function (data) {
                        swal("Correcto", "Orden de compra guardada con exíto. ", "success");
                        setTimeout(function () { location.href = "/getAllOrdenCompraByDia";; }, 2000)
                    }
                );
        });
    } else {
        //Swal.fire('Ha ocurrido un error', 'No debes dejar campos de la categoria vacios', 'error');
        showNotification("bg-red", err, "bottom", "right", "", "");
    }

}

function validarOrden() {
    if (proveedor == "" || proveedor == null) {
        return "Por favor, selecciona a un provedor. ";
    }
    if (materiales.length == 0) {
        return "Por favor, selecciona un material. ";;
    }
    return "ok";
}

function limpiarModalOrdenAgregar() {
    $('#txtNombrePOV').text("-");
    $('#txtCantidadMaterialOV').val(1);
    $('#txtSubtotalMaterialOV').val(1);
    $('#txtTotalOrdenAgregar').text("-");

    proveedor = "";
    materiales =[];
    llenarTablaDetalleMaterialOrden();
}
