$$
\begin{align}
\text{<int\_lit>} 		&\to \text{int\_lit}\\
\text{<str\_lit>} 		&\to \text{str\_lit}\\
\text{<statement>} 	&\to \text{<exit>}\space|\space
                         \text{<if>}  \space|\space
                         \text{<strout>}\\
\text{<exit>} 		&\to exit\space\text{<int\_lit>};\\
\text{<strout>} 		&\to strout\space\text{<str\_lit>};\\
\text{<if>} 		&\to if\space\text{<cond>}:\space\text{<statement>}
\end{align}
$$