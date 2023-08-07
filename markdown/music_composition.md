# generative music composition

To generate music we first collect and format the data we need for training.

We need to decide how we tokenize the data 


{{< lilypond >}}
\score{
    \relative c'' {
        % some notes
        g8 e \tuplet 3/2 { f[ a c] } e d a b c4
    }
    \layout{}
}
{{< \lilypond >}}
