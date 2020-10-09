const btnEveryone = $('#btn-everyone');
const btnPerson = $('.btn-person');

btnPerson.click(function () {
  console.log('qwe!')

  const personSlug = $(this).attr('data-person-slug');
  const personColor = $(this).attr('data-person-color');
  const personDuties = $('.' + personSlug);

  const btnEnabled = $(this).children('input').is(':checked');
  if (btnEnabled) {
    personDuties.css('background-color', personColor);
  } else {
    personDuties.css('background-color', '');
  }


});
