function posterior = computePosterior(X)

xfixed = X;
a = 0.6;
b = 0.2;
mu = 1.0*10^-99;
% mu = 0;
t1 = 5*10^6;
t2 = 5*10^6;
t3 = 7*10^6;
t4 = 2*10^6;
P = [0 0.2 0.6 0.2; 0.2 0 0.2 0.6; 0.6 0.2 0 0.2; 0.2 0.6 0.2 0];
I = [1 0 0 0; 0 1 0 0; 0 0 1 0; 0 0 0 1];

Q = P - I;

Pt1 = expm(Q*t1*mu);
Pt2 = expm(Q*t2*mu);
Pt3 = expm(Q*t3*mu);
Pt4 = expm(Q*t4*mu);
disp(Pt1);
disp(Pt2);
disp(Pt3);
disp(Pt4);

numerator = 0;
denominator = 0;

% A = 1, C = 2, G = 3, T = 4
for y = 1:4
    numerator = numerator + 0.25*Pt4(xfixed,y)*Pt1(y,1)*Pt2(y,1)*Pt3(xfixed,2);
    fprintf('numerator = %f\n', numerator)
    for x = 1:4
       denominator = denominator + 0.25*Pt4(x,y)*Pt1(y,1)*Pt2(y,1)*Pt3(x,2);
       fprintf('denominator = %f\n', denominator)
    end
end

posterior = numerator/denominator;

end