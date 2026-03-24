chrome.runtime.onMessage.addListener(

 async (data)=>{

  let response =
  await fetch(

   "https://your-api-url/best_card_for_txn",

   {

    method:"POST",

    headers:{

     "Content-Type":"application/json"

    },

    body:JSON.stringify({

     card_ids:[
      "icici_amazon",
      "hdfc_regalia_gold"
     ],

     amount:5000,

     category:"online_shopping"

    })

   }

  )

  let result = await response.json()

  document.getElementById("result").innerText =

   result.recommended_card

 }
)
