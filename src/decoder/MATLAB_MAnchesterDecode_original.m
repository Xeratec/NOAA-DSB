%% *LOAD - load raw IQ data and prepare for decoding
%
clear all;
%clf;
%hfile = 'POES_56k250.raw';
%hfile = 'pll_nocarrier_polyphased_equalized_loproto2.raw';
hfile = '../test/9_bits_dcblock.raw'; 
fid = fopen(hfile,'rb');
y = fread(fid,'float32');

y = (y(1:2:end) + 1i*y(2:2:end))';
%y = y(2:2:end) + 1i*y(1:2:end);
Nfft = 1500000;
%GNUradio should generate 1 sample per symbol with a period of
%- (1 /(8320*2)) Seconds per sample
Ts = 1/(8320*2);
RawTime=0:Ts:Ts*(numel(y)-1);
fclose(fid);
% %% CONSTELLATION - plot bit strengths
% pointScale = 501;
% length(y(1:pointScale:end));
% scatter(RawTime(1:pointScale:end),imag(y(1:pointScale:end)),[],'.');
% axis tight;
% %% CONSTELLATION - Show 10000 points again and again as run
% %the constellation should be two points VERTICALLY ALIGNED else swap I/Q above
% figure(1);
% colormap copper;
% Nfft = 100000+Nfft;
% x = y(Nfft:10000+Nfft);
% c = linspace(1,10,length(x));
% scatter(real(x),imag(x),[],c);
% xlabel('real');
% ylabel('imag');
% axis([-2 2 -2 2]);
% 
% %% CONSTELLATION - Animate
% figure(1);
% colormap copper;
% scatter(1,1);
% 
% axis([-2 2 -2 2]);
% numPoints=1000;
% c = linspace(1,10,numPoints+1);
% 
% for Nfft=1:numPoints:numel(y)-numPoints
%     x = y(Nfft:numPoints+Nfft);
%     scatter(real(x),imag(x),[],c);
%     axis([-2 2 -2 2]);
%     text(-1.8,1.8,num2str(RawTime(Nfft)));
%     %grid on;
%     %Nfft
%     drawnow
% end
%% *CONSTELLATION - Decode to raw bits
%convert constellation to bits
clear bitstream;
bitstream = uint8(zeros(1,numel(y)));
for idx = 1:numel(y)
    if(imag(y(idx)) > 0) %reverse if sync words are inverted
        bitstream(idx) = '1';
    else
        bitstream(idx) = '0';
    end
end

%% *CONSTELLATION - convert to bits from raw manchester bits
bitThreshold = 0.8;
idx2=1;
clockmod = 0;
idxerr=1;
%idxerr2=1;
clear errx erry bitstream_manchester BitTime;
bitstream_manchester(1) = uint8(0);
for idx = 2:numel(bitstream)-1
    %If not a bit boundary, see if it should be and we're out of sync
    %But only resync on strong bits
    if(mod(idx,2) ~= clockmod)    
        if(bitstream(idx-1) == bitstream(idx))
            errx(idxerr)=idx2;
            erry(idxerr)=real(y(idx));
            idxerr=idxerr+1;   
            if(abs(imag(y(idx-1))) > bitThreshold && abs(imag(y(idx))) > bitThreshold)                
                clockmod = mod(idx,2); %only resync if we have confidence in the bit decisions
            end
            
        end        
    end
    
    %check for bit boundary, and make decision using the strongest of the
    %two bits. 
    if(mod(idx,2) == clockmod)
        if(abs(imag(y(idx))) > abs(imag(y(idx+1)))) %use the strongest symbol to determine bit
            if(bitstream(idx) == '1')                
                bitstream_manchester(idx2) = '0';
            else
                bitstream_manchester(idx2) = '1';
            end
        else
            if(bitstream(idx+1) == '1')                
                bitstream_manchester(idx2) = '1';
            else
                bitstream_manchester(idx2) = '0';
            end        
        end
        
        BitTime(idx2)=RawTime(idx);    
        idx2 = idx2+1;
        %bitstream_manchester(idx2) = bitstream(idx+1);
                               
        
        %if(bitstream(idx-1) == bitstream(idx))
        %    errx(idxerr)=idx2;
        %    erry(idxerr)=real(y(idx));
        %    idxerr=idxerr+1;
        %end            
    end        
    
    %look for two same bits in a row
    %this can only happen on bit boundary
    %if we find this, resync to this boundary
    %if(bitstream(idx-1) == bitstream(idx))
    %    if(bitstream(idx) == 0)
    %        clockmod = mod(idx,2);
    %    end
    %end
end

%%plot autocorrelation to see if anything is here
%figure(2);
%subplot(2,1,1);
%plot(xcorr(bitstream))
%subplot(2,1,2);
%plot(xcorr(bitstream_manchester))

%%test autocorrelation of random number generator as reference
%testarray = rand(1,100000);
%for idx = 1:numel(testarray)
%    if(idx>0.5)
%        testarray2(idx) = 1;
%    else
%        testarray2(idx) = 0;
%    end
%end
%plot(xcorr(testarray2))

%% *BITSTREAM - Look for syncword and its inverse (in case of phase reversal)
SyncWord = '1110110111100010000'; %0100'; %NOAA15 ID last 4 0100
SyncWordInverse = '0001001000011101111'; %1011'; %NOAA15 ID

%S1 = '11101101111000100000 %1101'; %NOAA18 ID last 4 1101
%S2 = '00010010000111011111 0010'; %NOAA18 ID

SyncWordIndex = strfind(bitstream_manchester, SyncWord);
SyncWordInvIndex = strfind(bitstream_manchester, SyncWordInverse);
fprintf([ '\n' num2str(numel(SyncWordInvIndex)+numel(SyncWordIndex)) ' detected\n' num2str(sum(mod(diff(SyncWordIndex),832)==0) + sum(mod(diff(SyncWordInvIndex),832)==0)) ' match length\n\n' num2str(idxerr) ' errors\n\n']);
