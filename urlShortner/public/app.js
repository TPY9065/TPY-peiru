
var app = new Vue({
    el: '#app',
    data: {
      url: '',
      slug: '',
      err: ''
    },
    methods: {
        GenerateShortUrl(){
            console.log(`In app.js: ${this.url}`);
            fetch('/url', {
              body: JSON.stringify({
                url: this.url,
              }),
              headers: {
                'content-type': 'application/json'
              },
              method: 'POST'
            })
            .then( async (response) => {
              if (response.ok){
                await response.json()
                  .then( result => {
                    this.slug = `http://localhost:3000/${result.slug}`;
                    this.err = ''
                    console.log(`The created slug is ${this.slug}`);
                  })
              }else if (response.status == 500){
                await response.json()
                .then( result => {
                  this.err = result.message;
                })
              }
            })
        },
    }
  })