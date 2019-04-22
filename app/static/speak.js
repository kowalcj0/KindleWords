$(function(){
  speechSynthesis.onvoiceschanged = function() {
    var $voicelist = $('#voicelist');

    speechSynthesis.getVoices().forEach(function(voice, index) {
      var $voiceOption = $('<option>')
      .val(index)
      .html(voice.name);
      if (voice.lang.startsWith("en-")) {
        $voicelist.append($voiceOption);
      }
    });
  };
});

function speak(text){
  const msg = new SpeechSynthesisUtterance();
  const voices = window.speechSynthesis.getVoices();
  msg.voice = voices[$('#voicelist').val()];
  msg.text = text;

  msg.onend = function(e) {
    console.log('Finished speech synthesis for ' + this.text + ' in ' + event.elapsedTime + ' seconds.');
  };

  speechSynthesis.speak(msg);
}
