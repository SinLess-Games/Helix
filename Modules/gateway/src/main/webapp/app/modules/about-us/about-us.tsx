import './about-us.scss';

import React from 'react';
import { Translate } from 'react-jhipster';
import { connect } from 'react-redux';
import { Row, Col } from 'reactstrap';

export type IAboutUsProp = StateProps;

export const AboutUs = (props: IAboutUsProp) => {
  const { message } = props;

  return (
      <>
          <head>
              <title>About Sinless Games</title>
              <link href="//db.onlinewebfonts.com/c/3cec094dc3567ba25c8022f17affc2a1?family=Precious" rel="stylesheet" type="text/css"/>
          </head>
          <Row>
              <h1 className="titles">About US</h1>
              <Row className="container content-center">
                  <span className="hipster rounded content-center" />
              </Row>
              <Col md="1" />
              <Col md="10">
                  <Row className='div'>
                      <h2 className='container'>Our Story</h2>
                      <hr/>
                      <p className="text-justify">
                          SinLess Games is the Brain child of Timothy Pierce (CEO/Owner) The idea came to him during a discussion with friends about Games.
                          Timothy Had stated that games are lacking so much nowadays compared to what they used to be, referring to the fact that older games
                          relied more heavily on the story and plot to keep players attention rather than the graphics. &quot;Nowadays games lack a decent story
                          and even immersive qualities, they are so easy  to lose interest in that games have almost become dull.&quot; - Timothy Pierce 2019.
                          His friend, and entrepreneur and having started several of his own companies, responded with: &quot; well do something about it, start a game design company,
                          come up with a business plan, and learn how to make your own games and focus on what means the most for you.&quot; At this Timothy had thought
                          &ldquo; Not only was he right, but that was allot of work.&ldquo;
                      </p>
                      <p>
                          At this Timothy decided to take the leap and dive in to becoming and entrepreneur himself, but he would face many issues between his lack in motivation
                          to several learning disabilities. Though it was not easy He drove himself forward and in June of 2019 he registered SinLess Games LLC in the state of Montana.
                          He would continue building his company and expanding his own knowledge to drive his company forward.
                      </p>
                  </Row>
                  <Row className='div'>
                      <h2 className='container'>Our Philosophy</h2>
                      <hr/>
                      <p className="text-justify">
                          Here at SinLess Games we have but a few Philosophies:
                      </p>
                      <ul>
                          <li>Our products are made by gamers for gamers.</li>
                          <li>Immersion into our games&apos; worlds are a top priority.</li>
                          <li>Our Community&apos;s opinions matter.</li>
                          <li>Our products are made for you, with you in mind.</li>
                      </ul>

                  </Row>
                  <Row className='div'>
                      <h2 className='container'>What we have to Offer</h2>
                      <hr/>
                      <p className="text-justify">
                          We have many services to offer and more to come in the future below are what we offer at this time.
                      </p>
                      <ul>
                          <li>Gaming Desktop builds.</li>
                          <li>Custom Software</li>
                          <li>Our Learning Portal</li>
                          <li>Mentoring</li>
                      </ul>

                  </Row>
              </Col>
              <Col md="1" />
          </Row>
      </>
  );
};

const mapStateToProps = storeState => ({
  message: storeState.message,
});

type StateProps = ReturnType<typeof mapStateToProps>;

export default connect(mapStateToProps)(AboutUs);
