const smartDevice = /android|webos|iphone|ipad|ipod|blackberry|iemobile|opera mini/i.test(navigator.userAgent.toLowerCase());

let score = 0
const foundWords = new Set() // set for matching words found by the player
let s = 60 // seconds for timer
let hits = 0 // record number of times the player has played

$("#word").submit(handleSubmit) // listen for the player's text input events

$("footer").remove()

// GAME HANDLING
async function handleSubmit(e) {
    e.preventDefault();

    hits++

    console.log("event: ", e)

    const word = $("#guesstext").val()
    console.log("content: ", word)

    const resp = await axios.get("/check-word", { params: { word: word } })

    console.log("resp.data = ", resp.data)

    if (resp.data.result === "not-word") {
        console.log("1")
        messageResult(`${word} is not a valid English word`, "error")
    } else if (resp.data.result === "not-on-board") {
        console.log("2")
        messageResult(`${word} not on this board`, "error")
    } else {

        if (!foundWords.has(word)) {
            score += word.length
            $("#score").text(`score: ${score}`)
            foundWords.add(word)
            messageResult(`Added: ${word}`, "success")
        }
        else {
            messageResult(`${word} already found...`)
        }

    }
    $("#guesstext").val("") //clear the form 
}
function messageResult(message, cls) {
    console.log("message result = ", message)

    if (message != undefined) {
        if (message.includes("Added")) {
            // if (!smartDevice) {
            let msg = message.replace(/Added:/g, '') // capitalization done with css "text-transform:capitalize"
            $("#goodWords").append(`<li>${msg}</li>`).addClass(`messages ${cls}`)
            $("#wordstatus").text("GOOD WORK!").addClass(`messages ${cls}`)
            $("#wordstatus").css("font-size", "30px")
            setTimeout(() => { $("#wordstatus").empty() }, 500);
            // }
        }
        else {
            if (smartDevice) {
                alert(message)
            }
            else {
                $("#wordstatus").text(message).addClass(`messages ${cls}`)
                setTimeout(() => { $("#wordstatus").empty() }, 1500);
            }
        }
    }
}


// TIMER
$("document").ready(() => {
    if (location.href.includes("game_page")) {
        console.log("new game ready")
        setTimeInterval()
    }

    // don't show side containers if they're empty (must remember not to add return carriages in base.html)
    if ($('.sidecontent_l').text() === '') {
        $('.sidecontent_l').remove()
    }
    if ($('.sidecontent_r').text() === '') {
        $('.sidecontent_r').remove()
    }
})
async function setTimeInterval() {
    // const resp = await axios.get("/newBoggle")

    console.log("game started")

    if (smartDevice) // remove top and bottom (side) contents during game
    {

        $("#topContent").addClass("d-none") // just the game's name
        $("#sideContentLeft").addClass("d-none") // hall of fame
        // $("#sideContentRight").addClass("d-none") // found words... 
    }

    Interval0 = setInterval(timerHandler, 1000)

}
function timerHandler() {
    s--
    // console.log(s)
    if (s === 0) {
        $("#timer").text("GAME OVER!")
        endGameHandler()
        clearInterval(Interval0)
    }
    else {
        $("#timer").text(`${s} seconds left`)
    }
}

//END OF GAME
async function endGameHandler() {
    console.log("handling end game")

    if (smartDevice) // restore top and bottom (side) contents 
    {
        $("#topContent").removeClass("d-none")
        $("#sideContentLeft").removeClass("d-none")
        $("#sideContentRight").removeClass("d-none")
    }

    $(".boardbuttons").off("click") // remove board buttons event listner
    $("#word").off("submit") // remove submit form's event listener 
    $('#word').remove() // remove the form so as to prevent throwing errors on the back-end if user still tries to enter new words

    const resp = await axios.post("/endgame",
        {
            "hits": hits,
            "score": score
        })

    console.log("response:", resp.data)
    console.log("keys:", Object.keys(resp.data))
    console.log("values:", Object.values(resp.data))

    const obj = resp.data

    for (var key in obj) {
        console.log("game ", key)
        let game_numb = key
        let score = obj[key]["score"]
        let hits = obj[key]["hits"]

        if (smartDevice) {
            const div = $("<div>")
            div.attr("id", `game${game_numb}`).addClass("score_hist").text(`#${game_numb}: ${score}pts ${hits}hits`)
            $("#halloffame").append(div)
        } else {
            if (!smartDevice) $("#halloffame").append(`<li>Game# ${game_numb}: ${score} in ${hits} hits</li>`)
        }

    }

}

$(".boardbuttons").click(tdHandler)
let t = ""
function tdHandler(e) {
    e.preventDefault()
    let letter = $(e.target).text()
    console.log("letter => ", letter)
    // t += letter
    let input = $("#guesstext")
    input.val(input.val() + letter.toLowerCase())
}

document.addEventListener('DOMContentLoaded', function (event) {
    if (smartDevice) {
        $(".boardbuttons").css({
            "postion": "relative",
            "margin": "1px",
            "width": "30px",
            "height": "30px",
            "radius": "0px",
            "color": "black"
        })
    }
})