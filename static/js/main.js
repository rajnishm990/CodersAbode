let searchForm = document.getElementById('searchForm')
let pagelinks = document.getElementsByClassName('page-link')

if(searchForm){
    for(let i=0; pagelinks.length>i; i++){
        pagelinks[i].addEventListener('click' , function(e){
            e.preventDefault()
            let page= this.dataset.page

            searchForm.innerHTML += `<input value=${page} name="page" hidden/>`
            searchForm.submit()
        })
    }
}