function detalleVenta(idV) {
    var data = {
        idVenta: idV
    };
    $.ajax(
        {
            type: "GET",
            url: "/getAllVentasById",
            async: true,
            data: data
        })
        .done(
            function (data) {
                venta = data[0];
                console.log(venta)
                $('#txtNombreCliente').text(venta.cliente.idPersona.nombre + ' ' + venta.cliente.idPersona.apellidoP + ' ' + venta.cliente.idPersona.apellidoM);                
                $('#txtEmpleado').text(venta.user.nombre + ' ' + venta.user.apellidoP + ' ' + venta.user.apellidoM);                
                $('#txtNumeroCelularC').text(venta.cliente.idPersona.celular);
                $('#txtFechaVenta').text(venta.fecha_venta);
                $('#txtTotal').text(venta.total);
                detalleVentaP = venta.detalleVenta;
                $("#tbVentaDetalle > tbody").empty();
                for (var i = 0; i < detalleVentaP.length; i++){
                    $("#tbVentaDetalle>tbody").append('<tr><td class="text-center"> <img class="mb-4" src="'+ detalleVentaP[i].producto.img + '" alt="" width="120" height="95"></td><td>' + detalleVentaP[i].producto.modelo +'</td><td>' + detalleVentaP[i].producto.descripcion + '</td><td>'+ detalleVentaP[i].cantidad +'</td><td>'+ detalleVentaP[i].subtotal+'</td></tr>');
                }
                $('#modalDetalleVenta').modal('show');
            }
        );

}

function eliminarVenta(idV) {
    var data = {
        idVenta: idV
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
                url: "/deleteVenta",
                async: true,
                data: data
            })
            .done(
                function (data) {
                    swal('Movimiento realizado', 'Venta eliminada con exíto.', 'success');
                    setTimeout(function () { location.href = "/getAllVentasInactivas"; }, 2000)
                }
            );
    });

}
