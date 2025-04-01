function apagarObjeto(idProduto) {
  var confirmado = confirm("Tem certeza que quer apagar este objeto?");

  if (confirmado) {
    document.getElementById("form-apagar-" + idProduto).submit();
  }
}

function converterLead(idProduto) {
  let confirmado = confirm(
    "Tem certeza que quer converter este lead em cliente?",
  );
  if (confirmado) {
    document.getElementById("form-converter-" + idProduto).submit();
  }
}
