document.addEventListener("DOMContentLoaded", function(){
    var modal = document.getElementById("modalRedSocial");
    var abrirModal = document.getElementById("abrirModalRedSocial");
    var cerrarModal = document.getElementsByClassName("clsModRedSocial")[0];
    var btnCancelar = document.getElementById("btnCancelarRedSocial");

    abrirModal.onclick = function(event){
        event.preventDefault();
        var btnFileImage = document.getElementById("imagenRedSocialSubir");
        var imagenPreview = document.getElementById("previewImagen")

        btnFileImage.addEventListener("change", function(event){
            const file = event.target.files[0];

            if (file){
                if(file.type !== "image/svg+xml"){
                    alert("Solo se permite archivos de tipo SVG");
                    event.target.value = "";
                    return;
                }

                const reader = new FileReader();
                reader.onload = function(e){
                    imagenPreview.src = e.target.result;
                };
                reader.readAsDataURL(file);
            }else{
                imagenPreview.src = "#"
            }
        });
        
        modal.style.display = "block";
        document.body.style.overflow = "hidden";
    }

    cerrarModal.onclick = function(){
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    btnCancelar.onclick = function(){
        modal.style.display = "none";
        document.body.style.overflow = "auto";
    }

    /* FUNCION PARA LA PARTE DE EDICION DE LAS REDES SOCIALES*/
    var abirModalEditRedSocial = document.getElementById("modalEditRedSocial");
    var clsModalEditRedSocial = document.getElementsByClassName("clsModEditRedSocial")[0];
    var btnAbrirModalEditRedSocial = document.querySelectorAll(".btnAbrirModalEditRedSocial");
    var btnCancelarEditRedSocial = document.getElementById("btnCancelarEditRedSocial");

    btnAbrirModalEditRedSocial.forEach(btn => {
        btn.addEventListener("click", async (event) => {
            event.preventDefault();
            const data_id_atribute = event.target.getAttribute("data-id");
            console.log(data_id_atribute);

            try{
                const response = await fetch(`/ConsultalistaCatalogoRedes/${data_id_atribute}`);
                const data = await response.json();
                console.log(data);

                if (data.message === 'Success'){
                    
                    data.NombreRedesSociales.forEach(red => {
                        var baseURL = window.location.origin;
                        document.getElementById("previewImagenEdit").src = `${baseURL}/imagenes/${red.logo}`;
                        console.log(document.getElementById("previewImagen"))
                        document.getElementById("previewImagen").style.display = "block";
                        document.getElementById("redSocial_id").value = red.id;
                        document.getElementById("edit_nombre_redSocial").value = red.nombre_redSocial;
                    });
                }else{
                    console.log("Ocurrio un error")
                }
            }catch(e){
                console.log("Error", e);
            }

            abirModalEditRedSocial.style.display = "block"
            document.body.style.overflow = "hidden";

        });
    });

    clsModalEditRedSocial.addEventListener("click", function(){
        abirModalEditRedSocial.style.display = "none";
        document.body.style.overflow = "auto";
    });

    btnCancelarEditRedSocial.addEventListener("click", function(){
        abirModalEditRedSocial.style.display = "none";
        document.body.style.overflow = "auto";
    });

});