//script purpose: request a map link list from the server and create a
// gallery from which the user can choose a map

    document.addEventListener("DOMContentLoaded",async function(){response = await fetch("/api/get_template_files",{method: "POST"});
    data = await response.json();
    for (let i = 0; i < data.path_list.length; i++) {
      var img_id = "img"+i
      var image = document.getElementById(img_id);

      image.src = "static/" +data.path_list[i]
      image.alt = data.path_list[i]

      var link_text = "L"+i
      var link = document.getElementById(link_text);

      link.textContent = data.path_list[i];
      }
    })

    //dynamically creates the pages transition
    document.addEventListener("DOMContentLoaded",async function(){response = await fetch("/api/get_template_files",{method: "POST"});
    data = await response.json();
    const pages = [];
            const NumberOfPages = 1 +(Math.floor(data.path_list.length / 12))
            for (let i = 1; i <= NumberOfPages; i++) {
                pages.push({ value: 'page' + i, text: 'page ' + i });
            }
            AddPages(pages);
    })
     function AddPages(pages) {
            const select = document.getElementById('pages');
            pages.forEach(option => {
                const opt = document.createElement('option');
                opt.value = option.value;
                opt.textContent = option.text;
                select.appendChild(opt);
            });
        }
// loads the page chosen by the end user
function load_certain_page(event){
    const page_option = event.target.value;
    const page_number = parseInt(page_option.replace('page', ''));
    console.log(data.path_list)
    for (let i = (page_number-1)*12; i < data.path_list.length+(page_number-1)*12; i++) {
      console.log(i);
      console.log(i-(page_number-1)*12);
      var img_id = "img"+(i-(page_number-1)*12)
      var image = document.getElementById(img_id);
      if (i<data.path_list.length)
      {
        image.src = "static/" +data.path_list[(i)];
        image.alt = data.path_list[(i)];
      }
      else{
        image.src = "";
        image.alt = "";
      }
      var link_text = "L"+(i-(page_number-1)*12)
      var link = document.getElementById(link_text);
      link.textContent = data.path_list[(i)];
      }
}
document.getElementById('pages').addEventListener('change', load_certain_page);


//script purpose: send the server the designated map link, and also send
// the user to a page from which he can create a playable map from the template he clicked

    document.addEventListener("DOMContentLoaded", function() {
        // Get all link elements
        const links = document.querySelectorAll('.Template_gallery a');
        links.forEach(link => {
            link.addEventListener('click', function(event) {
                event.preventDefault();
                const linkText = link.textContent;
                const linkHref = link.href;
                fetch('/map_maker', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ link_text: linkText })
                })
                .then(() => {
                    window.location.href = linkHref;
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
            });
        });
    });
