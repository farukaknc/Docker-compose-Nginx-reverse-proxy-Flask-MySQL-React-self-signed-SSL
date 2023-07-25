import React from "react";

const ResultPage = props => (
    < div className="quiz-done" >
        <div
            className="message"
            style={{ color: 'green' }}
        >
            <>
                {props.isTimeUp ?
                    (
                        <div>
                            <h2>Time is up!</h2>
                            <h2>Quiz Results</h2>
                            <>
                                {props.score.length > 0 ?
                                    (<div>
                                        Your score is {props.score.reduce(function (acc, val) { return acc + val; }, 0)}/{props.totalscore}
                                    </div>) : (<div>Your score is 0/{props.totalscore}</div>)
                                }
                            </>
                        </div>
                    )
                    : (
                        <>
                            {
                                !props.isQuizPeriodUp ?
                                    (
                                        <div>
                                            <h2>The Quiz Period is up!</h2>
                                            <h2>Quiz Results</h2>
                                            {props.score.length > 0 ?
                                                (<div>
                                                    Your score is {props.score.reduce(function (acc, val) { return acc + val; }, 0)}/{props.totalscore}
                                                </div>) : (<div>Your score is 0/{props.totalscore}</div>)
                                            }
                                        </div>
                                    ) : (
                                        <div>
                                            <h2>Quiz Result</h2>
                                            {props.score.length > 0 ?
                                                (<div>
                                                    Your score is {props.score.reduce(function (acc, val) { return acc + val; }, 0)}/{props.totalscore}
                                                </div>) : (<div>Your score is 0/{props.totalscore}</div>)
                                            }
                                        </div>
                                    )

                            }
                        </>
                    )
                }
            </>
        </div>
    </div >
);

export default ResultPage;