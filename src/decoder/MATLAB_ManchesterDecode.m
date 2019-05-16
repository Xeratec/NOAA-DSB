%% *LOAD - load raw IQ data and prepare for decoding
clear all;

hfile = '../test/demod.raw'; 
%hfile = '../../RandomGnuRadioStuff/6_bits_dcblock2.raw';

fid = fopen(hfile,'rb');
y = fread(fid,'float32');
fclose(fid);

hfile2 = '../test/demod_imag.raw'; 
%hfile = '../RandomGnuRadioStuff/6_bits_dcblock2.raw';

fid2 = fopen(hfile2,'rb');
y2 = fread(fid2,'float32');
fclose(fid2);

y = (y(1:2:end) - 1i*y(2:2:end))';
Nfft = 15000;


%GNUradio should generate 1 sample per symbol with a period of
%- (1 /(8320*2)) Seconds per sample
Ts = 1/(8320*2);
RawTime=0:Ts:Ts*(numel(y)-1);


fprintf('Duration: %s\n', num2str(RawTime(end)))

% CONSTELLATION - plot bit strengths
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
bitstream01 = uint8(zeros(1,numel(y)));
for idx = 1:numel(y)
    if(imag(y(idx)) > 0) %reverse if sync words are inverted
        bitstream(idx) = '1';
        bitstream01(idx) = 1;
    else
        bitstream(idx) = '0';
        bitstream01(idx) = 0;
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
bitstream_manchester01(1) = uint8(0);
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
                bitstream_manchester01(idx2) = 0;
            else
                bitstream_manchester(idx2) = '1';
                bitstream_manchester01(idx2) = 1;
            end
        else
            if(bitstream(idx+1) == '1')                
                bitstream_manchester(idx2) = '1';
                bitstream_manchester01(idx2) = 1;
            else
                bitstream_manchester(idx2) = '0';
                bitstream_manchester01(idx2) = 0;
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

%% *BITSTREAM - Look for syncword and its inverse (in case of phase reversal)
SyncWord = '1110110111100010000'; %0100'; %NOAA15 ID last 4 0100
SyncWordInverse = '0001001000011101111'; %1011'; %NOAA15 ID

%S1 = '11101101111000100000 %1101'; %NOAA18 ID last 4 1101
%S2 = '00010010000111011111 0010'; %NOAA18 ID

SyncWordIndex = strfind(bitstream_manchester, SyncWord);
SyncWordInvIndex = strfind(bitstream_manchester, SyncWordInverse);
fprintf('#SyncWord: %d\n',numel(SyncWordIndex))
fprintf('#SyncWord (inverse): %d\n',numel(SyncWordInvIndex))
fprintf([ '\n' num2str(numel(SyncWordInvIndex)+numel(SyncWordIndex)) ' detected\n' num2str(sum(mod(diff(SyncWordIndex),832)==0) + sum(mod(diff(SyncWordInvIndex),832)==0)) ' match length\n\n' num2str(idxerr) ' errors\n\n']);


figure(3);
subplot(2,1,1);
%plot(k1,1:length(k1),'o',k2,1:length(k2),'x',errx,erry*10,'.');
plot(BitTime(SyncWordIndex),SyncWordIndex,'o',BitTime(SyncWordInvIndex),SyncWordInvIndex,'x',BitTime((errx(1:end-1))),erry(1:(end-1))*10,'.');
subplot(2,1,2);
plot(BitTime(SyncWordIndex(2:end)),diff(SyncWordIndex),'o',BitTime(SyncWordInvIndex(2:end)),diff(SyncWordInvIndex),'x',BitTime(errx(1:(end-1))),erry(1:(end-1))*10,'.');
%plot(k1(2:end),diff(k1),'o',k2(2:end),diff(k2),'x',errx,erry*10,'.');


%% *BITSTREAM -  convert ascii binary stream to actual binary at matched syncword locations
%Includes correct and inverted syncwords for periods of constellation reversal. 

clear minorFrames FrameTime;

SyncWordAllIndex = sort(cat(2,SyncWordIndex,SyncWordInvIndex));

for frameIdx=1:numel(SyncWordAllIndex)-1
    %See if the frame is normal or inverted bits
    if isempty(find(SyncWordInvIndex == SyncWordAllIndex(frameIdx),1))
        for frameByteIdx=0:103 %minor frames are 103 bytes long
            byte=0;
            %Start of byte time
            FrameTime(frameIdx,frameByteIdx+1)=BitTime(SyncWordAllIndex(frameIdx)+frameByteIdx*8);
            %if this is a normal sync word, use normal bits
            for bit_idx=0:7  %bytes are 8 bits long ;)                            
                if(bitstream_manchester(SyncWordAllIndex(frameIdx)+frameByteIdx*8+bit_idx)=='0')               
                    byte = bitshift(byte,1); %This is a zero, just shift           
                else                    
                    byte = bitshift(byte,1); %This is a one, set the bit then shift               
                    byte = bitor(byte,1);              
                end                
            end        
        minorFrames(frameIdx,frameByteIdx+1)=byte;    
        end
    else %this minor frame is inverted
        for frameByteIdx=0:103 %minor frames are 103 bytes long
            byte=0;
            %Start of byte time
            FrameTime(frameIdx,frameByteIdx+1)=BitTime(SyncWordAllIndex(frameIdx)+frameByteIdx*8);            
            for bit_idx=0:7  %bytes are 8 bits long ;)                            
                if(bitstream_manchester(SyncWordAllIndex(frameIdx)+frameByteIdx*8+bit_idx)=='0')               
                    byte = bitshift(byte,1); %This is a zero, just shift
                    byte = bitor(byte,1);              
                else                    
                    byte = bitshift(byte,1); %This is a one, set the bit then shift                                  
                end                
            end        
        minorFrames(frameIdx,frameByteIdx+1)=byte;    
        end
    end
end
%figure(4);
%plot(bitor(bitshift(bitand(minorFrames(:,5),1),8),minorFrames(:,6))); %plot minor frame counter, which is annoyingly 9 bits long
%plot(FrameTime(:,5),bitor(bitshift(bitand(minorFrames(:,5),1),8),minorFrames(:,6)),'.');

%% *BITSTREAM - Print Major Frame UTC times and spacecraft ID
clear minorFrameID dayNum spacecraftID;
minorFrameID = bitor(bitshift(bitand(minorFrames(:,5),1),8),minorFrames(:,6)); %pull out minor frame counter, which is annoyingly 9 bits long

figure(4);
plot(FrameTime(:,5),minorFrameID,'.'); %plot minor frame counter
spaceCraft(1) = 0;
dayNum(1) = 0;

idx = 1;

for frame=1:numel(minorFrameID)        
    spaceCraft(frame) = minorFrames(frame,3);    
    
    if(minorFrameID(frame) == 0)
        dayNum(idx)=bitshift(minorFrames(frame,8+1),1)+bitshift(bitor(minorFrames(frame,9+1),128),-7); %should be 241 for loproto2 recording        
        
        %check if the counter is more than the number of ms per day (bad data)
        if((bitshift(bitand(minorFrames(frame,9+1),bin2dec('111')),24) + bitshift(minorFrames(frame,10+1),16) + bitshift(minorFrames(frame,11+1),8) + minorFrames(frame,12+1)) < 86400000)
            dayMSeconds(idx) = (bitshift(bitand(minorFrames(frame,9+1),bin2dec('111')),24) + bitshift(minorFrames(frame,10+1),16) + bitshift(minorFrames(frame,11+1),8) + minorFrames(frame,12+1));
            fprintf([num2str(FrameTime(frame,1)) ' Local Seconds is ' num2str(dayMSeconds(idx)/1000.0) ' Spacecraft Day Seconds' ]);
            
            hour = floor(dayMSeconds(idx)/(1000*60*60));
            minute = floor((dayMSeconds(idx)/(1000*60*60) - hour)*60);
            seconds = (((dayMSeconds(idx)/(1000*60*60) - hour)*60) - minute) *60;
            fprintf([' which is ' num2str(hour) ':' num2str(minute) ':' num2str(seconds)]);
            
            if idx > 1 && dayMSeconds(idx) <= dayMSeconds(idx-1)
                fprintf(' ...but this might be an error');
            else
                hour = floor((dayMSeconds(idx)-FrameTime(frame,1)*1000)/(1000*60*60));
                minute = floor(((dayMSeconds(idx)-FrameTime(frame,1)*1000)/(1000*60*60) - hour)*60);
                seconds = ((((dayMSeconds(idx)-FrameTime(frame,1)*1000)/(1000*60*60) - hour)*60) - minute) *60;
                fprintf(['    t(0) => ' num2str(hour) ':' num2str(minute) ':' num2str(seconds)]);
            end
            fprintf('\n');
        else
            dayMSeconds(idx) = -1;
        end        
        idx = idx + 1;
        %fprintf([num2str(FrameTime(frame,1)) ':' num2str(dec2bin(minorFrames(frame,9+1),8)) ' ' num2str(dec2bin(minorFrames(frame,10+1),8)) ' ' num2str(dec2bin(minorFrames(frame,11+1),8)) ' ' num2str(dec2bin(minorFrames(frame,12+1),8)) '\n']);
        %fprintf([num2str(day) ' ' num2str(dec2hex(minorFrames(frame,8+1))) ' ' num2str(dec2hex(minorFrames(frame,9+1))) '\n\n']);        
    end
end

if mode(spaceCraft) == 8
   fprintf(['Spacecraft: ' num2str(mode(spaceCraft)) '=>NOAA-15\n']);    
   fprintf(['(Corrected) Day: ' num2str(mode(dayNum)-1) ' \n']);
elseif mode(spaceCraft) == 13
    fprintf(['Spacecraft: ' num2str(mode(spaceCraft)) '=>NOAA-18\n']);    
    fprintf(['(Corrected) Day: ' num2str(mode(dayNum)-1) ' \n']);
elseif mode(spaceCraft) == 15
    fprintf(['Spacecraft: ' num2str(mode(spaceCraft)) '=>NOAA-19\n']);    
    fprintf(['Day: ' num2str(mode(dayNum)) ' \n']);
else
    fprintf(['Spacecraft: ' num2str(mode(spaceCraft)) '=>A UFO!\n']);    
end


%% *PARITY - Run Partiy Check on frames
%Word 103
%Bit 1: CPU B data transfer incomplete bit
%Bit 2: CPU A data transfer incomplete bit
%Bit 3: Even parity check in words 2 through 18
%Bit 4: Even parity check in words 19 thru 35
%Bit 5: Even parity check in words 36 thru 52
%Bit 6: Even parity check in words 53 thru 69
%Bit 7: Even parity check in words 70 thru 86
%Bit 8: Even parity check in words 87 thru bit 7 of word 103

%Count ones. If the number of one's is odd, modulus will be 1. Even
%parity bit will be set to change the number of ones to be even, so the
%parity bit should match the modulus of the one count exactly. 
clear goodFrames parity;
parity = zeros(size(minorFrames,1),5);
goodFrames = 0;

for frame=1:size(minorFrames,1)
    parity(frame,1)=0;
    for word=3:19
        byte = minorFrames(frame,word);
           for shift=0:7
              parity(frame,1) = parity(frame,1)+bitand(bitshift(byte,-shift),1);   
           end       
    end
    
    for word=20:36           
        byte = minorFrames(frame,word);
           for shift=0:7
              parity(frame,2) = parity(frame,2)+bitand(bitshift(byte,-shift),1);   
           end       
    end
    
    for(word=37:53)           
        byte = minorFrames(frame,word);
           for(shift=0:7)
              parity(frame,3) = parity(frame,3)+bitand(bitshift(byte,-shift),1);   
           end       
    end
    
    for(word=54:70)           
        byte = minorFrames(frame,word);
           for(shift=0:7)
              parity(frame,4) = parity(frame,4)+bitand(bitshift(byte,-shift),1);   
           end       
    end
    
    for word=71:87
        byte = minorFrames(frame,word);
           for(shift=0:7)
              parity(frame,5) = parity(frame,5)+bitand(bitshift(byte,-shift),1);   
           end       
    end
        
    if(mod(parity(frame,1),2) == bitand(bitshift(minorFrames(frame,104),-5),1)) %check if divisible by 2 (even)       
        parity(frame,1) = 0; %words might be good or might have an even number of bit errors         
    else        
        parity(frame,1) = 1; %Words contain at least one error
    end    
        
    if(mod(parity(frame,2),2) == bitand(bitshift(minorFrames(frame,104),-4),1)) %check if divisible by 2 (even)       
        parity(frame,2) = 0; %words might be good or might have an even number of bit errors         
    else        
        parity(frame,2) = 1; %Words contain at least one error
    end
    
    if(mod(parity(frame,3),2) == bitand(bitshift(minorFrames(frame,104),-3),1)) %check if divisible by 2 (even)       
        parity(frame,3) = 0; %words might be good or might have an even number of bit errors         
    else        
        parity(frame,3) = 1; %Words contain at least one error
    end
    
    if(mod(parity(frame,4),2) == bitand(bitshift(minorFrames(frame,104),-2),1)) %check if divisible by 2 (even)       
        parity(frame,4) = 0; %words might be good or might have an even number of bit errors         
    else        
        parity(frame,4) = 1; %Words contain at least one error
    end
    
    if(mod(parity(frame,5),2) == bitand(bitshift(minorFrames(frame,104),-1),1)) %check if divisible by 2 (even)       
        parity(frame,5) = 0; %words might be good or might have an even number of bit errors         
    else        
        parity(frame,5) = 1; %Words contain at least one error
    end
    
    if sum(parity(frame,:)) == 0
        goodFrames = goodFrames + 1;
    end
end
fprintf([num2str(goodFrames) ' out of ' num2str(frame) ' Error Free Frames\n\n']);

%% PARITY - Plot results
figure(5);
clf;
%plot(1:size(parity,1),parity(:,1),'.-');
%plot(bitor(bitshift(bitand(minorFrames(:,5),1),8),minorFrames(:,6)));
plot(FrameTime(:,5),bitor(bitshift(bitand(minorFrames(:,5),1),8),minorFrames(:,6)),'.');
%Px=1:size(parity,1);
Px=FrameTime(:,1)';
Py=parity(:,1)'*512;
Pz = zeros(1,size(Px,2));
S = surface([Px;Px],[Py;Py],[Pz;Pz], 'facecol','no','edgecol','interp','linew',1.5,'edgealpha',.125,...
            'edgecolor',0*[1 1 1],...
            'facecolor',0*[1 1 1]);

%Px=1:size(parity,1);
%Px=FrameTime(:,1)';
Py=parity(:,2)'*512;
Pz = zeros(1,size(Px,2));
S = surface([Px;Px],[Py;Py],[Pz;Pz], 'facecol','no','edgecol','interp','linew',1.5,'edgealpha',.125,...
            'edgecolor',0.5*[.15 1 1],...
            'facecolor',0.5*[.15 1 1]);

%Px=1:size(parity,1);
Py=parity(:,3)'*512;
Pz = zeros(1,size(Px,2));
S = surface([Px;Px],[Py;Py],[Pz;Pz], 'facecol','no','edgecol','interp','linew',1.5,'edgealpha',.125,...
            'edgecolor',0.5*[1 .15 1],...
            'facecolor',0.5*[1 .15 1]);

 %Px=1:size(parity,1);
 Py=parity(:,4)'*512;
 Pz = zeros(1,size(Px,2));
 S = surface([Px;Px],[Py;Py],[Pz;Pz], 'facecol','no','edgecol','interp','linew',1.5,'edgealpha',.125,...
             'edgecolor',0.5*[1 1 .15],...
             'facecolor',0.5*[1 1 .15]);
 
%Px=1:size(parity,1);
Py=parity(:,5)'*512;
Pz = zeros(1,size(Px,2));
S = surface([Px;Px],[Py;Py],[Pz;Pz], 'facecol','no','edgecol','interp','linew',1.5,'edgealpha',.125,...
            'edgecolor',0.5*[.15 1 .15],...
            'facecolor',0.5*[.15 1 .15]);

axis([0 max(FrameTime(:,1)) -0.1 515]);
