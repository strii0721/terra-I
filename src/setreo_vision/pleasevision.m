%% Setup image input
frame = imread('C:\Users\lynchpin\repository\terra-I\resources\stereo_calibration\ball\left\1754054864.6690507-left.bmp');
frame = imresize(frame, [cameraParams.ImageSize(1), cameraParams.ImageSize(2)]);

%% Known Parameters
ball_diameter = 5; % cm

% Camera intrinsic parameters
f_x = cameraParams.FocalLength(1);
f_y = cameraParams.FocalLength(2);
c_x = cameraParams.PrincipalPoint(1);
c_y = cameraParams.PrincipalPoint(2);
focal_length = f_x; % for Z calc

% Buffer setup (even if not needed for single frame)
buffer = [];
bufferSize = 5;

%% Display figure
hFig = figure('Name','Object Tracker (Single Cam)');

if ishandle(hFig)
    % Undistort and convert
    frameUndist = undistortImage(frame, cameraParams);
    hsv = rgb2hsv(frameUndist);
    h = hsv(:,:,1); s = hsv(:,:,2); v = hsv(:,:,3);

    % Blue object segmentation
    mask = h > 0.55 & h < 0.62 & s > 0.6 & v > 0.4;
    mask = imclose(mask, strel('disk', 5));
    mask = imfill(mask, 'holes');
    mask = bwareaopen(mask, 200);

    % Find circular regions
    stats = regionprops(mask, 'Centroid', 'MajorAxisLength', 'MinorAxisLength', 'Eccentricity');
    

    % Circularity threshold (tighter)
    circularStats = stats([stats.Eccentricity] < 0.75 & ...
                       [stats.MajorAxisLength] > 10 & ...
                       [stats.MajorAxisLength] < 800);  % to avoid false detections

    if ~isempty(circularStats)
        [~, idx] = max([circularStats.MajorAxisLength]);
        c = circularStats(idx).Centroid;
        ball_size_pixels = circularStats(idx).MajorAxisLength;

        % Estimate depth (Z) from ball size in pixels
        Z = (ball_diameter * focal_length) / ball_size_pixels;

      
        % Project pixel coordinates to real-world (camera-centered) coordinates
        X = ((c(1) - c_x) * Z) / f_x;
        Y = -((c(2) - c_y) * Z) / f_y;  % invert Y because image Y increases down


        % Buffer not critical here, but included
        buffer = [buffer; [X, Y, Z]];
        if size(buffer, 1) > bufferSize
            buffer(1, :) = [];
        end

        % Display results
        imshow(frameUndist); hold on;
        plot(c(1), c(2), 'rx', 'MarkerSize', 12, 'LineWidth', 2);
        title(sprintf('Object at X=%.2f cm, Y=%.2f cm, Z=%.2f cm', X, Y, Z));
        hold off;
        fprintf('Pixel Centroid: (%.1f, %.1f)\n', c(1), c(2));
        fprintf('Ball size (pixels): %.1f\n', ball_size_pixels);
        fprintf('Estimated Position: X=%.2f cm, Y=%.2f cm, Z=%.2f cm\n', X, Y, Z);
    else
        imshow(frameUndist);
        title('Object not found');
    end
    drawnow;
end


