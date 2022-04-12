import './home.scss';

import React  from 'react';
import { Row, Col } from 'reactstrap';
/** import react carousel */
import "react-responsive-carousel/lib/styles/carousel.min.css";





import { useAppSelector } from 'app/config/store';

export const Home = () => {
  const account = useAppSelector(state => state.authentication.account);

  return (
    <>
        <Col className="showcase">
            <Row className="container content-center">
                <span className="hipster rounded content-center" />
            </Row>
            <Row className='container'>
                <h2>Welcome to SinLess Games LLC</h2>
                <p className='re'>welcome to SinLess Games LLC</p>
                <p className="moto">Where games and apps are made for gamers, by gamers. In a place where immersion ranks supreme!</p>
            </Row>
        </Col>
        <br/>
        <br/>
        <Row className="Container content-center">
            <Col className="container content-center">
                <img src="../../../content/images/keyboard.png" alt="keyboard" className="keyboard content-center" />
            </Col>
            <Col className="callToAction content-center">
                <Row className="container content-center">
                    <hr className="call2" />
                    <p className='p2'>
                        Join us in a world where anything becomes possible, a place where dreams can come true.
                        We plan to offer games that give you a vivid escape from reality.
                        Games that you can lose yourself in and forget about your problems even if just for a little bit.
                    </p>
                    <hr className="call2" />
                </Row>
            </Col>
        </Row>
        <br/>
    </>
  );
};

export default Home;
