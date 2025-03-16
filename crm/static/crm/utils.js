function apagarObjeto(idProduto) {
  var confirmado = confirm("Tem certeza que quer apagar este objeto?");

  if (confirmado) {
    document.getElementById("form-apagar-" + idProduto).submit();
  }
}
