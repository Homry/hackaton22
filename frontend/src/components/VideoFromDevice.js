import {Container, Table} from "react-bootstrap";


export default function VideoFromDevice() {

    // получить лист

    let list_videos = [ {"src": "vid1.mp4", "name": "some name"}, {"src": "vid2.mp4", "name": "some name"}]
    let video_arr = []

    for (let vid of list_videos){
        video_arr.push( <div key={vid["src"]}><video src={vid["src"]} controls width="40%">
            Sorry, your browser doesn't support embedded videos.
        </video></div>)
    }


    return (
        <Container>
            <Table>
                <thead />
                <tbody>
                {video_arr}

                </tbody>
            </Table>


        </Container>



    );
}
