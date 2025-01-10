document.addEventListener('DOMContentLoaded', function() {
  const buyButtons = document.querySelectorAll('.buy-btn');
 
   buyButtons.forEach(button => {
      button.addEventListener('click', function() {
           const productId = this.getAttribute('data-product-id');
             window.location.href = `/buy/${productId}`;
       });
   });
 
     const checkoutForm = document.getElementById('checkoutForm');

       checkoutForm.addEventListener('submit', function(event) {
         event.preventDefault(); 

         alert('თქვენს ამანათს 5-7 სამუშაო დღეში მიიტანენ ფილიალში.');


          checkoutForm.reset();

  });

});