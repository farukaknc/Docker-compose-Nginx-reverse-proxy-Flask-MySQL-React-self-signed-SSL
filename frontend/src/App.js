import React, { Component, useState, useEffect } from 'react';
import './App.css';
import axios from "axios"
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import { Button, CardActions, ButtonGroup } from '@mui/material';

import QuestionCount from './components/QuestionCount';
import Header from './components/Header';
import ResultPage from './components/ResultPage';
import Question from './components/Question';
import AnswerOptions from './components/AnswerOptions';
import PreviousButton from './components/PreviousButton';
import NextButton from './components/NextButton';
import SubmitButton from './components/SubmitButton';
import CountdownTimer from './components/CountdownTimer';
import QuestionList from './components/QuestionList';


function App() {

  const [dbQuestions, setDbQuestions] = useState([])
  const [quizAttributes, setQuizAttributes] = useState([])

  const [loading, setloading] = useState(undefined);
  const [completed, setcompleted] = useState(undefined);
  const [infoPage, setInfoPage] = useState(undefined);
  const [useremail, setUserEmail] = useState('');
  const [username, setUserName] = useState('');
  const [checkIPfrombcknd, setCheckIPfrombcknd] = useState('');

  useEffect(() => {
    setTimeout(() => {
      fetch('http://127.0.0.1:5000/api', {
        'method': 'GET'
      })
        .then(resp => resp.json())
        //.then(resp => console.log(resp.questions))
        .then(resp => {
          setDbQuestions(resp.questions);
          setQuizAttributes(resp.quiz);
          setloading(true)
          setTimeout(() => {
            setcompleted(true)
          }, 1000);
        })
        .catch(error => console.log(error))
    }, 2000);
  }, [])
  const [clientIP, setClientIP] = useState("False");

  useEffect(() => {
    const fetchClientIP = async () => {
      try {
        const response = await fetch('https://api.ipify.org?format=json');
        if (response.ok) {
          const data = await response.json();
          setClientIP(data.ip);
        } else {
          console.error('Failed to fetch IP address.');
        }
      } catch (error) {
        console.error('Error fetching IP address:', error);
      }
    };

    fetchClientIP();
  }, []);



  //const sleep = ms => new Promise(r => setTimeout(r, ms));


  const checkIP = async (quizId, ipAddress) => {
    const url = `http://127.0.0.1:5000/api/checkIP?quizId=${quizId}&ipAddress=${ipAddress}`;

    console.log(quizId);
    console.log(ipAddress);

    try {
      const response = await axios.get(url);

      setCheckIPfrombcknd(response.data);
      //console.log(response.data.results)
      //await sleep(4000)
      //console.log('Response from backend:', response.data);
      setloading(true);
      setcompleted(true);
    } catch (error) {
      console.error('Error sending GET request:', error);
    }



  };

  const handleCheckIP = () => {
    checkIP(quizAttributes[0]["QuizID"], clientIP)
  }


  return (
    console.log(checkIPfrombcknd),
    <>
      {!completed ? (
        <>
          {!loading ? (
            <div className="spinner">
              <span>Loading...</span>
              <div className="half-spinner"></div>
            </div>
          ) : (
            <div className="completed">&#x2713;</div>
          )}
        </>
      ) : (
        <>
          {
            !infoPage ? (
              <div style={{ display: 'flex', justifyContent: 'center', paddingTop: '150px' }}>
                <Card sx={{ minWidth: 690 }}>
                  <CardContent>
                    <Typography gutterBottom variant="h5" component="div">
                      Quiz - {dbQuestions[0]["Course_Name"]}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      <li>Duration: {quizAttributes[0]["Duration"]}</li>
                      <li>Number of Questions: {quizAttributes[0]["NumofQuestions"]}</li>
                      <li>Total Score: {quizAttributes[0]["TotalScorePossible"]}</li>
                    </Typography>
                  </CardContent>
                  <CardActions>
                    <ButtonGroup variant="contained" aria-label="outlined primary button group">

                      <Button size="small" color="primary" onClick={() => {
                        setInfoPage(true);
                        setUserEmail("example@gmail.com");
                        setUserName("Faruk");
                        setcompleted(false);
                        setloading(false);
                        handleCheckIP();
                      }}>
                        Start the Quiz
                      </Button>
                    </ButtonGroup>
                  </CardActions>
                </Card>
              </div>
            ) : (

              <>
                {
                  checkIPfrombcknd === "False" ? (
                    <>
                      <QuizApp dbQuestions={dbQuestions} quizAttributes={quizAttributes} useremail={useremail} username={username} clientIP={clientIP} />
                    </>


                  ) : (
                    < div className="quiz-done" >
                      <div
                        className="message"
                        style={{ color: 'green' }}
                      >
                        <div>
                          <h3>You have already finished this quiz!</h3>
                          <h2>Quiz Results</h2>
                          <div>Your score is {0}/{50}</div>

                        </div>
                      </div>
                    </div>
                  )
                }
              </>

            )
          }
        </>
      )}
    </>
  );
}


class QuizApp extends Component {
  constructor(props) {
    super(props);
    const arr = []
    const Qlist = []
    for (let i = 0; i < this.props.dbQuestions.length; i++) {
      arr.push('')
      Qlist.push({
        question: `Q${i + 1}`,
        status: `Not Answered`,
        qCounter: i
      })
    }
    this.state = {
      questions: [{
        questionId: 1000,
        question: "Which of the following is NOT a type of research design commonly used in empirical research?",
        answers: ["Experimental", "Narrative", "Correlational", "different"],
        correctAnswer: "Narrative",
        courseName: "Empirical Research 1",
        questionScore: 25
      },
      {
        questionId: 1001,
        question: 'Which of the following is NOT a type of research design commonly used in empirical research?',
        answers: ["different1", "different2", "different3", "different4"],
        correctAnswer: "Narrative",
        courseName: "Empirical Research 1",
        questionScore: 25
      }],
      questionCounter: 0,
      timeUp: false,
      periodUp: false,
      header: 'Empirical Research 1',
      questionId: 1,
      hours: 0,
      minutes: 0,
      seconds: 0,
      questionList: Qlist,
      givenAnswers: Array(this.props.dbQuestions.length).fill(''),
      totalScore: arr,
      quizStatus: 'active',
      startingTime: new Date().getTime(),
      quizQuestions: this.props.dbQuestions,
      quizID: 1000, //this.props.quizAttributes[0]["QuizID"],
      selectedOption: ''
    }
    this.totalPoScore = this.calculateTotalPoScore.bind(this)
    this.onAnswerClick = this.onAnswerClick.bind(this)
    this.handlePrevButton = this.handlePrevButton.bind(this)
    this.handleNextButton = this.handleNextButton.bind(this)
    this.handleSubmitButton = this.handleSubmitButton.bind(this)
    this.onDropOptionSelected = this.onDropOptionSelected.bind(this)
    this.postQuizData = this.postQuizData.bind(this)
  }

  calculateTotalPoScore(quizQuestions) {
    var total = 0
    for (var i = 1; i <= quizQuestions.length; i++) {
      total += quizQuestions[i - 1].questionScore
    }
    return total
  }

  componentDidMount() {
    //console.log(this.state.quizQuestions)

    //console.log(this.state.questions[this.state.questionCounter].answers.map(answer => console.log(answer)))
    setInterval(() => {

      let difference = this.state.startingTime + (this.props.quizAttributes[0]["Duration"] * 60 * 1000) - new Date();
      if (difference < 1 | ((new Date()) > (new Date(this.props.quizAttributes[0]["Quiz_End_Time"].replace(" GMT", ""))))) {
        this.setState({ timeUp: true });
        this.setState({ periodUp: true });
        this.setState(state => {
          const totalScore = state.givenAnswers.map((item, j) => {
            if (item === this.state.questions[j]["correctAnswer"]) {
              return this.state.questions[j]["questionScore"]
            } else {
              return 0
            }
          });

          return {
            totalScore,
            quizStatus: 'finished',
          };
        });

        this.setState(state => {
          const givenAnswers = state.givenAnswers.map((item, j) => {
            if (j === this.state.questionCounter) {
              return this.state.selectedOption;
            } else {
              return item;
            }
          });

          return {
            selectedOption:
              this.state.givenAnswers[this.state.questionCounter + 1] !== ''
                ? this.state.givenAnswers[this.state.questionCounter + 1]
                : '',
            givenAnswers,
          };
        });

      } else {
        let hours = Math.floor((difference / (1000 * 60 * 60)) % 24);
        let minutes = Math.floor((difference / (1000 * 60)) % 60);
        let seconds = Math.floor((difference / (1000)) % 60);
        const dataArray = this.props.dbQuestions.map(item => ({
          questionid: item.Question_ID,
          question: item.Question_Desc,
          answers: [item.Choice1, item.Choice2, item.Choice3, item.Choice4, item.Choice5, item.Choice6],
          correctAnswer: item.Correct_Answer,
          courseName: item.Course_Name,
          questionScore: item.Question_Score
        }))

        const arr = []
        const Qlist = []
        for (let i = 0; i < dataArray.length; i++) {
          arr.push('')
          Qlist.push({
            question: `Q${i + 1}`,
            status: `Not Answered`,
            qCounter: i
          })
        }

        this.setState({
          hours: hours > 9 ? hours : `0${hours}`,
          minutes: minutes > 9 ? minutes : `0${minutes}`,
          seconds: seconds > 9 ? seconds : `0${seconds}`,
          questions: dataArray,
          questionList: Qlist
        });
      }
    }, 1000)

  }

  onAnswerClick(content) {
    this.setState(state => {
      const givenAnswers = state.givenAnswers.map((item, j) => {
        if (j === this.state.questions.length - 1 && this.state.questionCounter + 1 === this.state.questions.length) {
          return content;
        } else {
          return item;
        }
      });

      return {
        selectedOption: content,
        givenAnswers,
      };
    });
  }

  onDropOptionSelected(qCounter) {
    this.setState(state => {
      const givenAnswers = state.givenAnswers.map((item, j) => {
        if (j === this.state.questionCounter) {
          return this.state.selectedOption;
        } else {
          return item;
        }
      });

      return {
        selectedOption:
          this.state.givenAnswers[qCounter] !== ''
            ? this.state.givenAnswers[qCounter]
            : '',
        givenAnswers,
        questionCounter: qCounter,
      };
    });
  }


  handlePrevButton() {
    this.setState(state => {
      const givenAnswers = state.givenAnswers.map((item, j) => {
        if (j === this.state.questionCounter) {
          return this.state.selectedOption;
        } else {
          return item;
        }
      });

      return {
        selectedOption:
          this.state.givenAnswers[this.state.questionCounter - 1] !== ''
            ? this.state.givenAnswers[this.state.questionCounter - 1]
            : '',
        givenAnswers,
        questionCounter: this.state.questionCounter - 1,
      };
    });
  }

  handleNextButton() {
    this.setState(state => {
      const givenAnswers = state.givenAnswers.map((item, j) => {
        if (j === this.state.questionCounter) {
          return this.state.selectedOption;
        } else {
          return item;
        }
      });

      return {
        selectedOption:
          this.state.givenAnswers[this.state.questionCounter + 1] !== ''
            ? this.state.givenAnswers[this.state.questionCounter + 1]
            : '',
        givenAnswers,
        questionCounter: this.state.questionCounter + 1,
      };
    });
  }

  handleSubmitButton() {
    this.setState(state => {
      const givenAnswers = state.givenAnswers.map((item, j) => {
        if (j === this.state.questionCounter) {
          return this.state.selectedOption;
        } else {
          return item;
        }
      });

      return {
        selectedOption:
          this.state.givenAnswers[this.state.questionCounter] !== ''
            ? this.state.givenAnswers[this.state.questionCounter]
            : '',
        givenAnswers,
      };
    });
    this.setState(state => {
      const totalScore = state.givenAnswers.map((item, j) => {
        if (item === this.state.questions[j]["correctAnswer"]) {
          return this.state.questions[j]["questionScore"]
        } else {
          return 0
        }
      });

      return {
        totalScore,
        quizStatus: 'finished',
      };
    });

    this.postQuizData()

  }

  postQuizData() {

    let arr = []

    let resultArr = [
      this.props.quizAttributes[0]["QuizID"],
      this.props.clientIP, // add student name property after adding a login page
      3286, // student ID
      this.state.questions.length,
      this.state.questions.length, //change this afterwards
      this.state.totalScore.reduce(function (acc, val) { return acc + val; }, 0)
    ]

    for (let i = 1; i <= this.state.questions.length; i++) {
      arr.push([
        this.props.quizAttributes[0]["QuizID"],
        this.state.header,
        this.state.questions[i - 1]["questionid"], // question id
        this.props.clientIP, // add student name property after adding a login page
        3286, // student ID
        i, // question number
        this.state.givenAnswers[i - 1],
        this.state.questions[i - 1]["correctAnswer"]
      ])
    }
    //console.log({ arr, resultArr })
    axios.post("http://127.0.0.1:5000/addUserLogResults", { body: { arr, resultArr } })
      .then(response => response.json())
      .catch(err => {
        console.error(err.response); //err.toJSON()
      });
  }



  render() {
    return (
      <div className="quiz-app">
        {this.state.quizStatus === 'active' && !this.state.timeUp ? (
          <div className='body'>
            <Header header={this.state.header} />
            <div className='rowC'>
              <QuestionCount
                counter={this.state.questionCounter + 1}
                totalCount={this.props.dbQuestions.length}
              />
              <div key={this.state.questionId} className='container'>
                <div className='question-options'>
                  <Question
                    questionId={this.state.questionId}
                    questions={this.state.questions}
                    counter={this.state.questionCounter}
                  />
                  <ul className="answerOptions">
                    {this.state.questions[this.state.questionCounter].answers?.map(answer => (
                      answer !== '' ?
                        <AnswerOptions
                          key={answer}
                          answerContent={answer}
                          questionId={this.state.questionId}
                          givenAnswers={this.state.givenAnswers}
                          correctAnswer={this.state.correctAnswer}
                          onClick={this.onAnswerClick}
                          counter={this.state.questionCounter}
                          selectedOption={this.state.selectedOption}
                        />
                        : null
                    ))}
                  </ul>
                </div>
                <div className="button-container">
                  <PreviousButton
                    onClick={this.handlePrevButton}
                    counter={this.state.questionCounter}
                  />
                  {this.state.questionCounter + 1 === this.props.dbQuestions.length ? (
                    <SubmitButton
                      onClick={this.handleSubmitButton}
                    />
                  ) : (
                    <NextButton
                      onClick={this.handleNextButton}
                      counter={this.state.questionCounter}
                      totalQuestion={this.props.dbQuestions.length}
                    />
                  )}
                </div>
              </div>
              <div className='rowD timer'>
                <div className='time-left'>Time Left</div>
                <CountdownTimer
                  hours={this.state.hours}
                  minutes={this.state.minutes}
                  seconds={this.state.seconds}
                />
                <div className='rowE'>
                  <QuestionList
                    qList={this.state.questionList}
                    placeHolder="Go to Question..."
                    onOptionClick={this.onDropOptionSelected}
                  />
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div>
            <Header header={this.state.header} />
            <ResultPage
              score={this.state.totalScore}
              totalscore={this.calculateTotalPoScore(this.state.questions)}
              isTimeUp={this.state.timeUp}
              isQuizPeriodUp={this.state.periodUp}
            />
          </div>
        )
        }
      </div>
    )
  }
}

export default App;
