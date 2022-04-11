import './home.scss';

import React  from 'react';
import { Link } from 'react-router-dom';
import { Translate } from 'react-jhipster';
import { Row, Col, Alert } from 'reactstrap';



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
      <Row className="content-center">
        <Col>
          <span className="keyboard rounded content-center" />
        </Col>
        <Col className="callToAction rounded content-center">
          <div>
            <Row>
              <hr className="call2" />
            </Row>
            <Row className="container content-center">
              <p className='p2'>
                Join us in a world where anything becomes possible, a place where dreams can come true.
                We plan to offer games that give you a vivid escape from reality.
                Games that you can lose yourself in and forget about your problems even if just for a little bit.
              </p>
            </Row>
            <Row>
              <hr className="call2" />
            </Row>
          </div>
        </Col>
      </Row>
    </>
  );
};

export default Home;
